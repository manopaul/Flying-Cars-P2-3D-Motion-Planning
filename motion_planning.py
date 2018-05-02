import argparse
import time
import msgpack
from enum import Enum, auto

import numpy as np

from planning_utils import a_star, heuristic, create_grid, get_lat_lon, prune_path
from udacidrone import Drone
from udacidrone.connection import MavlinkConnection
from udacidrone.messaging import MsgID
from udacidrone.frame_utils import global_to_local

class States(Enum):
    MANUAL = auto()
    ARMING = auto()
    TAKEOFF = auto()
    WAYPOINT = auto()
    LANDING = auto()
    DISARMING = auto()
    PLANNING = auto()

class MotionPlanning(Drone):

    def __init__(self, connection, goal_position=None):
        super().__init__(connection)

        self.target_position = np.array([0.0, 0.0, 0.0])
        self.waypoints = []
        self.in_mission = True
        self.check_state = {}

        # initial state
        self.flight_state = States.MANUAL
        self.goal_position = goal_position

        # register all your callbacks here
        self.register_callback(MsgID.LOCAL_POSITION, self.local_position_callback)
        self.register_callback(MsgID.LOCAL_VELOCITY, self.velocity_callback)
        self.register_callback(MsgID.STATE, self.state_callback)

    def local_position_callback(self):
        if self.flight_state == States.TAKEOFF:
            if -1.0 * self.local_position[2] > 0.95 * self.target_position[2]:
                self.waypoint_transition()
        elif self.flight_state == States.WAYPOINT:
            if np.linalg.norm(self.target_position[0:2] - self.local_position[0:2]) < 1.0:
                if len(self.waypoints) > 0:
                    self.waypoint_transition()
                else:
                    if np.linalg.norm(self.local_velocity[0:2]) < 1.0:
                        self.landing_transition()

    def velocity_callback(self):
        if self.flight_state == States.LANDING:
            if self.global_position[2] - self.global_home[2] < 0.1:
                if abs(self.local_position[2]) < 0.01:
                    self.disarming_transition()

    def state_callback(self):
        if self.in_mission:
            if self.flight_state == States.MANUAL:
                self.arming_transition()
            elif self.flight_state == States.ARMING:
                if self.armed:
                    self.plan_path()
            elif self.flight_state == States.PLANNING:
                self.takeoff_transition()
            elif self.flight_state == States.DISARMING:
                if ~self.armed & ~self.guided:
                    self.manual_transition()

    def arming_transition(self):
        self.flight_state = States.ARMING
        print("arming transition")
        self.arm()
        self.take_control()

    def takeoff_transition(self):
        self.flight_state = States.TAKEOFF
        print("takeoff transition")
        self.takeoff(self.target_position[2])

    def waypoint_transition(self):
        self.flight_state = States.WAYPOINT
        print("waypoint transition")
        self.target_position = self.waypoints.pop(0)
        print('target position', self.target_position)
        self.cmd_position(self.target_position[0], self.target_position[1], self.target_position[2], self.target_position[3])

    def landing_transition(self):
        self.flight_state = States.LANDING
        print("landing transition")
        self.land()

    def disarming_transition(self):
        self.flight_state = States.DISARMING
        print("disarm transition")
        self.disarm()
        self.release_control()

    def manual_transition(self):
        self.flight_state = States.MANUAL
        print("manual transition")
        self.stop()
        self.in_mission = False

    def send_waypoints(self):
        print("Sending waypoints to simulator ...")
        data = msgpack.dumps(self.waypoints)
        self.connection._master.write(data)

    def plan_path(self):
        self.flight_state = States.PLANNING
        print("Searching for a path ...")
        TARGET_ALTITUDE = 5
        SAFETY_DISTANCE = 5 #5

        self.target_position[2] = TARGET_ALTITUDE

        # TODO: read lat0, lon0 from colliders into floating point values
        filename = 'colliders.csv'
        # TODO: set home position to (lon0, lat0, 0)
        home_lat, home_lon = get_lat_lon(filename)
        #print(home_lat, home_lon)
        self.set_home_position(home_lon, home_lat, 0)

        # TODO: retrieve current global position
        current_global_position = [self._longitude, self._latitude, self._altitude]
        #print('Current global position : {}'.format(current_global_position))

        # TODO: convert to current local position using global_to_local()
        local_north, local_east, local_down = global_to_local(current_global_position, self.global_home)
        print('Global Home {0}, Position {1}, Local Position {2}'.format(self.global_home, self.global_position, self.local_position))

        # Read in obstacle map
        data = np.loadtxt('colliders.csv', delimiter=',', dtype='Float64', skiprows=3)

        # Define a grid for a particular altitude and safety margin around obstacles
        grid, north_offset, east_offset = create_grid(data, TARGET_ALTITUDE, SAFETY_DISTANCE)
        print("North offset = {0}, East offset = {1}".format(north_offset, east_offset))

        # TODO: convert start position to current position rather than map center
        # Define starting point on the grid (this is just grid center)
        # grid_start = (-north_offset, -east_offset)
        grid_start_N = int(np.ceil(local_north - north_offset))
        grid_start_E = int(np.ceil(local_east - east_offset))
        grid_start = (grid_start_N, grid_start_E)

        #print('grid_start_N : {}'.format(grid_start_N))
        #print('grid_start_E : {}'.format(grid_start_E))
        #print('grid_start : {}'.format(grid_start))

        # Set goal as some arbitrary position on the grid
        #grid_goal = (-north_offset + 475, -east_offset - 400)
        #grid_goal = (-north_offset + 10, -east_offset + 10)
        # This is passed in as arguments in the main method
        # Defaults to the lat and lon of Gateway Theatre (37.796725 -122.400071)
        #print("goal_position: {}".format(self.goal_position))
        # TODO: adapt to set goal as latitude / longitude position and convert

        goal_north, goal_east, goal_alt = global_to_local(self.goal_position, self.global_home)
        grid_goal_N = int(np.ceil(goal_north - north_offset))
        grid_goal_E = int(np.ceil(goal_east - east_offset))
        grid_goal = (grid_goal_N, grid_goal_E)

        #print('grid_goal_N : {}'.format(grid_goal_N))
        #print('grid_goal_E : {}'.format(grid_goal_E))
        #print('grid_goal : {}'.format(grid_goal))

        print('Local Start and Goal : ', grid_start, grid_goal)

        print('Determining the most complete and optimal path. Please be patient')

        # Run A* to find a path from start to goal
        # TODO: add diagonal motions with a cost of sqrt(2) to your A* implementation
        # or move to a different search space such as a graph (not done here)
        path, _ = a_star(grid, heuristic, grid_start, grid_goal)
        print('Length of found Path : {}'.format(len(path)))

        # TODO: prune path to minimize number of waypoints
        # TODO (if you're feeling ambitious): Try a different approach altogether!
        pruned_path = prune_path(path)
        print('Length of pruned path: {}'.format(len(pruned_path)))

        # Convert path to waypoints
        waypoints = [[p[0] + north_offset, p[1] + east_offset, TARGET_ALTITUDE, 0] for p in pruned_path]
        # Set self.waypoints
        self.waypoints = waypoints
        # TODO: send waypoints to sim
        self.send_waypoints()

    def start(self):
        self.start_log("Logs", "NavLog.txt")

        print("starting connection")
        self.connection.start()

        # Only required if they do threaded
        # while self.in_mission:
        #    pass

        self.stop_log()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5760, help='Port number')
    parser.add_argument('--host', type=str, default='127.0.0.1', help="host address, i.e. '127.0.0.1'")
    # The Gateway Theatre 37.796725 -122.400071
    parser.add_argument('--goal_latitude', type=str, default='37.796725', help="Latitude of the goal, i.e. '37.796725'")
    parser.add_argument('--goal_longitude', type=str, default='-122.400071', help="Longitude of the goal, i.e. '-122.400071'")
    parser.add_argument('--goal_altitude', type=str, default='0.', help="Altitude of the goal, i.e. '0.'")
    args = parser.parse_args()

    conn = MavlinkConnection('tcp:{0}:{1}'.format(args.host, args.port), timeout=60)
    goal_position = (float(args.goal_longitude), float(args.goal_latitude), float(args.goal_altitude))
    drone = MotionPlanning(conn, goal_position=goal_position)
    time.sleep(1)

    drone.start()

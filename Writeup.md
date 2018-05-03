## Project: 3D Motion Planning
![Trajectory Image](./images/Trajectory%20Flight.png)
---

In this 3D Motion planning, the concepts of planning a trajectory by discretizing the environment for search, grid and graph representation of the enviroment, obstacle representations from collider files, A* search algorithm, converting global to local coordinates, and optimization using collinearity checks are addressed.

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  
You're reading it! Below I describe how I addressed each rubric point and where in my code each point is handled. How to run this project is specified in the README.md file.

### Explain the Starter Code

#### 1. Explain the functionality of what's provided in `motion_planning.py` and `planning_utils.py`
The starter code includes 2 python script files - motion_planning.py and planning_utils.py.
These scripts contain a basic planning implementation for a flying car to fly in a zig zag manner from start to goal. It includes state transitions that were part of the backyard flyer project. These include: 
arming transition,
takeoff transition,
waypoint transition,
landing transition, and
disarming transition

These state transition methods was augmented by implementing the planning state after arming and before takeoff state transition.

### Implementing Your Path Planning Algorithm

#### 1. Set your global home position

The latitude and longitude values are given in the first line of the collider.csv file.
In the planning.py file, a function to get the latitude and longitude was written. See line  in planning.py.
The filename was passed to this method and the first line was read and the latitude and longitude values were read using string manipulation code. 
The extracted latitude (lat0) and longitude (lon0) values owas then set as the global home position (self.set_home_position()) in the motion_planning.py file as shown in lines 121-126. 
https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L121

#### 2. Set your current local position
In order to determine the local position relative to the global home position, the current global position is first determined using the latitude, longitude and altitude as shown in line XXX of the motion_planning.py file. 
Then using the global_to_local function in the planning.py (lines XXX), the current global position is converted to the local position which comprises of the NED frame (local North, local East, and local Altitude) as shown in lines XXX of the motion_planning file. 

#### 3. Set grid start position from local position
The obstacles information was read from the provided colliders file to create a grid for a particular altitude and safety margins around the obstacles. When the configuration space (grid) was created, the north and east offset was determined. Then by subtracting the respective offsets from the local north and local east position, the grid start north and grid start east positions were computed to determine th grid start position from the local position. 
Lines XXX in the motion_planning.py file show this.

#### 4. Set grid goal position from geodetic coords
The goal position is provided as parameter arguments in the main method as latitude and longitude arguments. If not goal arguments are passed, the program defaults to the Gateway Theatre location. The goal position along is converted to local position in the same manner as the grid start position and both the grid start and the grid goal position are passed to the A* algorithm to determine to determine the path from the start to the goal. 
Lines XXX in the motion_planning.py file show these. 

#### 5. Modify A* to include diagonal motion (or replace A* altogether)
The planning_utils.py was modified to include diagonal motions on the grid with a cost of sqrt(2) as shown in lines XXX. Additionally, the file was modified to account of valid actions to cover NORTH_EAST, NORTH_WEST, SOUTH_EAST and SOUTH_WEST motion in addition to the NORTH, EAST, WEST and SOUTH directions. 
Lines XXX in the planning_utils.py file show these. 

#### 6. Cull waypoints 
Using the A* algorithm, a trajectory path (waypoints) from start to goal position is determined. However, if two waypoints lie on the same line, then it would be suboptimal for the flying car (drone) to go through each waypoint and center itself relative to that waypoint. So a collinearity check is done and waypoints that are in line between the first and last waypoint in that line are culled (pruned) and a new pruned path is computed from the path. Lines XX show this.
The top down view image shows the paths with the linear waypoints culled from a bird's eye view perspective. 
![Top Down View](./images/Bird's%20Eye%20View.png)

### Execute the flight
#### 1. Does it work?
You should be able to observe what is shown in the video below

[![3D Motion Planning](http://img.youtube.com/vi/u61VaB3Qmqk/0.jpg)](https://youtu.be/u61VaB3Qmqk)


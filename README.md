## Project: 3D Motion Planning

---
In this 3D Motion planning, the concepts of planning a trajectory by discretizing the environment for search, grid and graph representation of the enviroment, obstacle representations from collider files, A* search algorithm, converting global to local coordinates, and optimization using collinearity checks are addressed.

The top down image shows the paths from a bird's eye view perspective. 
![Top Down View](./images/Bird's%20Eye%20View.png)

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
In the planning.py file, a function to get the latitude and longitude was written. 
The filename was passed to this method and the first line was read and the latitude and longitude values were read using string manipulation code.
See lines [163-175](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/planning_utils.py#L163) in planning_utils.py.
The extracted latitude (lat0) and longitude (lon0) values were then set as the global home position (self.set_home_position()) in the motion_planning.py file as shown in line [126](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L126)

#### 2. Set your current local position
In order to determine the local position relative to the global home position, the current global position is first determined using the latitude, longitude and altitude as shown in line [129](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L129) of the motion_planning.py file. 
Then using the global_to_local function from the udacidrone.frame_utils, the current global position is converted to the local position which comprises of the NED frame (local North, local East, and local Down (altitude)) as shown in line [133](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L133) of the motion_planning.py file. 

#### 3. Set grid start position from local position
The obstacles information was read from the provided colliders file to create a grid for a particular altitude and safety margins around the obstacles. When the configuration space (grid) was created, the north and east offset was determined. Lines [136-141](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L136) in the motion_planning.py file show this.
Then by subtracting the respective offsets from the local north and local east position, the grid start north and grid start east positions were computed to determine th grid start position from the local position. 
Lines [143-152](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L143) in the motion_planning.py file show this.

#### 4. Set grid goal position from geodetic coords
The goal position is provided as parameter arguments in the main method as latitude and longitude arguments. If no goal arguments are passed, the program defaults to the Gateway Theatre location. See lines [209-217](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L209) for this implementation. The goal position is converted to local position in the same manner as the grid start position. Lines [162-171](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L162) in the motion_planning.py file shows this implementation. 
Both the grid start and the grid goal position are passed to the A* algorithm to determine to determine the path from the start to the goal.  Lines [178](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L178) in the motion_planning.py file shows this implementation. 

#### 5. Modify A* to include diagonal motion (or replace A* altogether)
The planning_utils.py was modified to include diagonal motions on the grid with a cost of sqrt(2) as shown in lines [60-63](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/planning_utils.py#L60). Additionally, the file was modified to account for valid actions to cover NORTH_EAST, NORTH_WEST, SOUTH_EAST and SOUTH_WEST motion in addition to the NORTH, EAST, WEST and SOUTH directions. Lines [94-101](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/planning_utils.py#L94) in the planning_utils.py file show this. 

#### 6. Cull waypoints 
Using the A* algorithm, a trajectory path (waypoints) from start to goal position is determined. However, if two waypoints lie on the same line, then it would be suboptimal for the flying car (drone) to go through each waypoint and center itself relative to that waypoint. So a collinearity check is done and waypoints that are in the same line between the first and last waypoint in that line are culled (pruned) and a new pruned path is computed from the path. Lines [183](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L183) shows this. The prune path method that does the collinearity check is defined in lines [191-212](https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/planning_utils.py#L191) of the planning_utils.py file.
The trajectory image below shows the paths with the linear waypoints culled out. 
![Trajectory Image](./images/Trajectory%20Flight.png)

### Execute the flight
#### 1. Does it work?
A video clip showing the 3D Motion Planning working code is shown below.
![3D Motion Planning Clip](./images/3D%20Motion%20Planning.gif)

The video can be found here: [3D Motion Planning Video](https://youtu.be/u61VaB3Qmqk)

---
## Running the Project
---

## To run this project on your local machine, follow these instructions:
### Step 1: Download the Simulator
This is a new simulator environment!  
Download the Motion-Planning simulator for this project that's appropriate for your operating system from the [simulator releases respository](https://github.com/udacity/FCND-Simulator-Releases/releases).

### Step 2: Clone and Activate the fcnd environment
1. By cloning the FCND-Term1-Starter-Kit directory, set up the virtual environment locally and activate it using the following command  
   `source activate fcnd`  

### Step 3: Clone and Activate the fcnd environment
2. Clone the 3d motion planning repository  
   `git clone https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning.git`  
3. Download and run the Simulator and click on the Motion Planning icon  
4. Open a Terminal window and run the following command  
  `python motion_planning.py`  



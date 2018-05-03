## Project: 3D Motion Planning
![Trajectory Image](./images/Trajectory%20Flight.png)

---
In this 3D Motion planning, the concepts of planning a trajectory by discretizing the environment for search, grid and graph representation of the enviroment, obstacle representations from collider files, A* search algorithm, converting global to local coordinates, and optimization using collinearity checks are addressed. 

---
### Writeup / README

#### 1. Provide a Writeup / README that includes all the rubric points and how you addressed each one.  

You're reading it! Below I describe how I addressed each rubric point and where in my code each point is handled.

### Explain the Starter Code

#### 1. Explain the functionality of what's provided in `motion_planning.py` and `planning_utils.py`
The starter code includes 2 python script files - motion_planning.py and planning_utils.py.
These scripts contain a basic planning implementation that includes...



Here's | A | Snappy | Table
--- | --- | --- | ---
1 | `highlight` | **bold** | 7.41
2 | a | b | c
3 | *italic* | text | 403
4 | 2 | 3 | abcd

### Implementing Your Path Planning Algorithm

#### 1. Set your global home position

The latitude and longitude values are given in the first line of the collider.csv file.
In the planning.py file, a function to get the latitude and longitude was written. See line  in planning.py.
The filename was passed to this method and the first line was read and the latitude and longitude values were read using string manipulation code. 
The extracted latitude (lat0) and longitude (lon0) values owas then set as the global home position (self.set_home_position()) in the motion_planning.py file as shown in lines 121-126. 
https://github.com/manopaul/Flying-Cars-P2-3D-Motion-Planning/blob/master/motion_planning.py#L121

#### 2. Set your current local position
Here as long as you successfully determine your local position relative to global home you'll be all set. Explain briefly how you accomplished this in your code.

In order to determine the local position relative to the global home position, the current global position is first determined using the latitude, longitude and altitude as shown in line XXX of the motion_planning.py file. 
Then using the global_to_local function in the planning.py (lines XXX), the current global position is converted to the local position which comprises of the NED frame (local North, local East, and local Altitude) as shown in lines XXX of the motion_planning file. 

Meanwhile, here's a picture of me flying through the trees!
![Forest Flying](./misc/in_the_trees.png)

#### 3. Set grid start position from local position
This is another step in adding flexibility to the start location. As long as it works you're good to go!

#### 4. Set grid goal position from geodetic coords
This step is to add flexibility to the desired goal location. Should be able to choose any (lat, lon) within the map and have it rendered to a goal location on the grid.

#### 5. Modify A* to include diagonal motion (or replace A* altogether)
Minimal requirement here is to modify the code in planning_utils() to update the A* implementation to include diagonal motions on the grid that have a cost of sqrt(2), but more creative solutions are welcome. Explain the code you used to accomplish this step.

#### 6. Cull waypoints 
For this step you can use a collinearity test or ray tracing method like Bresenham. The idea is simply to prune your path of unnecessary waypoints. Explain the code you used to accomplish this step.


![Top Down View](./images/Bird's%20Eye%20View.png)

### Execute the flight
#### 1. Does it work?
It works!

### Double check that you've met specifications for each of the [rubric](https://review.udacity.com/#!/rubrics/1534/view) points.
  
# Extra Challenges: Real World Planning

For an extra challenge, consider implementing some of the techniques described in the "Real World Planning" lesson. You could try implementing a vehicle model to take dynamic constraints into account, or implement a replanning method to invoke if you get off course or encounter unexpected obstacles.



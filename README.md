# AIG240_Project2_JetAuto_Control
My submission for AIG240 Project 2. In which, we write a Python script to move a JetAuto robot in a square sequence in Gazebo.

## Assessment Questions

1. What command did you use to launch the JetAuto robot in Gazebo? <br>
   `roslaunch jetauto_gazebo worlds.launch`
2. Which two other launch files were called when you launched worlds.launch? Hint: Do not use GenAI to answer this because it does not have access to the file. Inspect the launch files in jetauto_ws/src/jetauto_simulation/jetauto_gazebo/launch. <br>
   `spwan_model.launch` and `room_worlds.launch`
3. Describe the process of setting up your ROS workspace and creating the project package. <br>
  I. I made a workspace directory called `project2_ws` and a subdirectory called `src`. In the `project2_ws` directory I used the command `catkin_make` and `source devel/setup.bash` to intitialize and source the workspace. <br>
  II. In `~/project2_ws/src`, I used the command `catkin_create_pkg project2 rospy geometry_msgs` to create a package directory called `project2` and install the necessary packages `rospy` and `geometry_msg`. I also made a directory inside the package directory called `scripts`, where the package will pull the .py scripts from. <br>
  III. I copy and pasted the old controller script from Project 1 into `~/project2_ws/src/project2/scripts`. Since the file I copied was already executable, I did not have to make it executable via commandline or permissions. <br>
  IV. I retured to `~/project2_ws` and reran `catkin_make` and `source devel/setup.bash` to update the source files to match the current package. I reran `source devel/setup.bash` after every edit to jetauto_control.py to ensure that the package is configured to the new edits. <br>
5. (Answer this only if you completed the advanced turning option) What challenges did you face with making the robot move in a straight line while turning, and how did you overcome them? <br>
One of the hardest challenges was modelling the drift motion equations. In order to make the drift work, the angular motion must overtake the linear motion but not so much that the robot veers from its linear path. The way that real cars achieve drift is by either braking (decreasing linear velocity) or steering harder (increasing angular velocity). The equations that I found to work best were to decrease the linear velocity linearly, and to have the angular velocity increase as a quadratic. I also found it challenging to adjust the parameters such that the motion follows the path that we want. To get the results that I have, it took a lot of trial an error and knowing what parameter to adjust and whether to increase or decrease to get the result I wanted.

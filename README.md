# EE260C_LAB0: Access Carla

Please refer to the instructions [here](https://docs.google.com/document/d/1PwzTUXI43FQObJ2Cy7xu3a_J-AEyEal76FWF_SttEhE/edit?usp=sharing)

# Lab 0 ReadMe
## Setup
Refer to Lab 0 instructions to setup a conda environment. Make sure to active it. Then, start a CARLA simulator.

## Traffic Manager
Run `python3 traffic_manager.py`. Feel free to comment and/or uncomment the sections that run vehicles on autopoilot and that run vehicles on a set trajectory.

## Bounding Boxes
Run `python3 bounding_boxes.py`. Feel free to commment and/or uncomment the section that draws 2D bbox and writes to the PASCAL VOC format.

## Instance Segmentation
Run `python3 instance_segmentation.py`. Change `cam_location`, `cam_rotation`, and the save path as you wish. If a segfault occurs, the instance segmentation image should still save.
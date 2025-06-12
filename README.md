# Carla VR Streaming

## Setup
- Start a docker CARLA simulator container using the instructions [here](https://github.com/UCR-CISL/Carla-dockers)
- Make sure to run `xhost +` before running the docker container so we can connect to the simulator

## Manual Control + Streaming
- Run ```manual_control_streaming.py``` once the Carla simulator has been started in the background
- Will start a websocket on `ws://0.0.0.0:<port (default is 8765)>`
- Values can be changed [here](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/main/manual_control_streaming.py#L315)
- Websocket will send each frame from the [VR camera](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/main/manual_control_streaming.py#L1394C13-L1394C17)
- It will also [receive current headset orientation](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/028093afc9c29aa198c56b6f42a43d3e757108de/manual_control_streaming.py#L248) through the websocket and [update the VR camera transforms](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/028093afc9c29aa198c56b6f42a43d3e757108de/manual_control_streaming.py#L1477) to mimic head rotation
- Vehicle is [hard-coded](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/028093afc9c29aa198c56b6f42a43d3e757108de/manual_control_streaming.py#L333) so that the camera position is always inside the car. Camera positon can also be changed [here](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/028093afc9c29aa198c56b6f42a43d3e757108de/manual_control_streaming.py#L1394)
- Head rotation values come from the [CarlaVR Unity app](https://github.com/skyguy-netizen/CarlaVR) which should be built and running on the headset


## Inputs
- Input method is currently set to the LogiTech Wheel and Pedals as defined in [SteeringWheelControl](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/028093afc9c29aa198c56b6f42a43d3e757108de/manual_control_streaming.py#L757) class
- You can change input method to KeyBoardControl in the code block [here](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/028093afc9c29aa198c56b6f42a43d3e757108de/manual_control_streaming.py#L1736-L1755)
- Wheel config is in `wheel_config.ini`
- There was an issue where the Steering Wheel would stop working all of a sudden. It was because the sensitivity is calculated using both max and min values from the config, but if they are the same, then the sensitivity would go to 0. That code block has been commented out [here](https://github.com/skyguy-netizen/CarlaVRStreaming/blob/028093afc9c29aa198c56b6f42a43d3e757108de/manual_control_streaming.py#L889-L897), and the current code only relies on the max value defined in the config 

## Tip on driving in Carla
- Don't crash :)

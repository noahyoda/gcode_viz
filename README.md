# singed_slices

## How to run
- cd into script directory
- run `python3 render.py`
- enjoy :\)

## Advanced Controls
- to specify a gcode file to run, use -f \<path-to-file>
- to specify how many layers to simulate, use -n \<nth layer> to only simulate every nth layer (default is 10 to save resources)

 **Warning -**
Increasing the value of n will decrease the resolution of the simulation. It is recommended to not use lower n values if you are short on ram or want to simulate larger data sets. If the simulation is running slow we recommend increasing the value of n.

## Controls
#### Zoom in/out
- mouse scroll up/down
#### Rotate
- click and drag mouse
#### Slide (left/right/up/down)
- arrow keys
#### Play/Pause Simulation
- space bar

## Tasks Complete
- Write project description
- Setup git and other project tools
- Generate simple cube sample gcode
- Write script to parse gcode
- Write Progress Report
- write shape viewing script
- write simulation drawing script
- extract temp and speed from gcode script

## Progress
- finish heat diffusion script
- write [final report](https://www.overleaf.com/project/642da1880c0552fdb4473e66)

## Project Board 
- https://trello.com/b/f7vdvp7X/project-overview

## Resources
- https://pypi.org/project/pygcode/0.1.0/
- https://www.pygame.org/docs/
- https://marlinfw.org/meta/gcode/

#### 3d Files
- [Arch](https://www.thingiverse.com/thing:2135190)
- [Octopus](https://www.thingiverse.com/thing:3495390)
- [Teapot](https://www.thingiverse.com/thing:821)

#### Gcode File(s)
- [Fullcontrol Pin Support](https://fullcontrol.xyz/#/models/67cf20)
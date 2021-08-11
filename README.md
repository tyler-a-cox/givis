# Giant Impact Visualization

I'm going to build a command line tool interface which will be the only thing
that's exposed to the user. Install the command line tool in base python, find the users
blender installation and install those dependencies, then call blender in a subprocess

## Assets
![Example Simulation](assets/full_pressure.gif)
![Example Simulation](assets/full_pressure_3D.gif)
![Example Simulation](assets/pressure_sliced.gif)

## Setup
Install [Blender 2.79](https://download.blender.org/release/Blender2.79/)

### MacOS
`export PATH=$PATH:/Applications/Blender/blender.app/Contents/MacOS`

### Linux
`blender -b -P setup.py`

## Run
`givis`

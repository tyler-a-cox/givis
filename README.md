# Giant Impact Visualization

I'm going to build a command line tool interface which will be the only thing
that's exposed to the user. Install the command line tool in base python, find the users
blender installation and install those dependencies, then call blender in a subprocess

## Assets

### Full Simulation
<p align="center">
  <img src="assets/full_pressure.gif" alt="animated" />
</p>

### 3D Option
<p align="center">
  <img src="assets/full_pressure_3D.gif" alt="animated" />
</p>

### Slice Along Axis
<p align="center">
  <img src="assets/pressure_sliced.gif" alt="animated" />
</p>

## Setup
This package requires [Blender](https://download.blender.org/release/Blender2.79/) to be installed.
Blender handles the majority of the raytracing while this packages handles camera movement,
particle position, data manipulation, and 

### MacOS
`export PATH=$PATH:/Applications/Blender/blender.app/Contents/MacOS`

### Linux
`blender -b -P setup.py`

## Run
`givis`

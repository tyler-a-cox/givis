# Giant Impact Visualization

Giant Impact Visualization is a Python package built on top of the Blender API used for visualizing the output of Smoothed Particle Hydrodynamics simulations of giant planetary impacts (although this code is probably generalizable to other SPH simulations). Specifically, this package allows the user to quickly produce a visualization of their data, customize the color map, plot by variable type (temperature, pressure, etc.), and apply cuts to the data. 

## Assets
Here are a few examples of the different customizations you can apply to your data. The simulation below is a full run (~500,000 particles) of two planetary bodies colliding with the color map denoting log pressure. In addition to a full run, the user can also render their animation in 3D and slice along specified axes to see a cross-section of the data.

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
This package requires [Blender](https://download.blender.org/release/Blender2.79/) to be installed before installing. Blender handles the majority of the raytracing while this packages handles camera movement, particle position, data manipulation, and normalization. After installing Blender, run the following commands to install the package

```
git clone https://github.com/tyler-a-cox/givis
cd givis
python setup.py install
```


## Run
To run the code, simply use the command line argument `givis`. For a full description of the customizable features run the command below

`givis --help`

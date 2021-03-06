import subprocess
import sys
from pathlib import Path
import setuptools

# Install necessary packages in blender's python installation
subprocess.call(["blender", "-b", "-P", "blender_setup.py"])
setuptools.setup(
    name="givis",
    version="1.0",
    scripts=["./scripts/givis"],
    author="Tyler Cox",
    description="Python package that renders giant impact simulation data",
    packages=["givis"],
    python_requires=">=3.5",
)

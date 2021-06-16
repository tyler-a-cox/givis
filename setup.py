import subprocess
import sys
from pathlib import Path

try:
    import bpy

except ImportError:
    print(
        "Module 'bpy' could not be imported. This probably means you are not using Blender to run this script."
    )
    sys.exit(1)

# OS independent (Windows: bin\python.exe; Mac/Linux: bin/python3.7m)
py_path = Path(sys.prefix) / "bin"
print(py_path)


# first file that starts with "python" in "bin" dir
py_exec = next(py_path.glob("python*"))
# ensure pip is installed & update
print(py_exec)


subprocess.call([str(py_exec), "-m", "ensurepip"])
subprocess.call([str(py_exec), "-m", "pip", "install", "--upgrade", "pip"])
# install dependencies using pip
# dependencies such as 'numpy' could be added to the end of this command's list

packages = ["matplotlib", "scipy"]

for p in packages:
    subprocess.call(
        [
            str(py_exec),
            "-m",
            "pip",
            "install",
            "--trusted-host",
            "pypi.python.org",
            "--trusted-host",
            "files.pythonhosted.org",
            p,
        ]
    )

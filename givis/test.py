import os
import sys
import bpy

dir = os.path.dirname(bpy.data.filepath)
if not dir in sys.path:
    sys.path.append(dir)

import space_view3d_point_cloud_visualizer

# print(sys.path)

# import space_view3d_point_cloud_visualizer

print(os.getcwd())
print(__name__)

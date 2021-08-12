import bpy
import tqdm
import numpy as np
import matplotlib.pyplot as plt
from .space_view3d_point_cloud_visualizer import PCVControl, PCV_OT_render
import os

# Load in Data
positions = np.load("../data/positions_x1Downsample_pos.npy", mmap_mode="r")
temp = np.load("../data/positions_x1Downsample_Temp.npy", mmap_mode="r")


class PointCloudVisualizer:
    """Method for visualizing
    """

    def __init__(
        self, positions: str, temperature: str, blend_file: str = "untitled.blend"
    ):
        """
        """
        self.positions = np.load(positions, mmap_mode="r")
        self.temperature = np.load(temperature, mmap_mode="r")

        bpy.ops.wm.save_as_mainfile(filepath=blend_file)
        o = bpy.context.active_object
        self.c = PCVControl(o)
        self.pcv = bpy.context.object.point_cloud_visualizer
        self.pcv.render_path = os.path.join(os.getcwd(), "render/####")
        self.pcv.render_point_size = 4
        self.pcv.alpha_radius = 0.75

    def log_normalize(
        self,
        temperature,
        T_min: float = 1300,
        T_max: float = 1e4,
        scalar: float = 11604.0,
    ) -> float:
        """
        Normalize a variable array on a log scale

        Args:
            T_min: minimum float value in the normalization
            T_max: maximum float value in the normalization
            scalar: scalar applied to data post normalization

        Returns:
            log_T_ceiling_norm: normalized array
        """
        T_ceiling = np.copy(temperature) * 11604.0
        T_ceiling[np.where(T_ceiling > T_max)] = T_max
        T_ceiling[np.where(T_ceiling < T_min)] = T_min
        log_T_ceiling = np.log10(T_ceiling) - np.log10(T_min)
        log_T_ceiling_norm = log_T_ceiling / (np.log10(T_max) - np.log10(T_min))
        return log_T_ceiling_norm

    def set_render_settings(
        self,
        anaglyph: bool = False,
        cyan: bool = False,
        camera_location: tuple = (40, -20, 20),
        camera_rotation: tuple = (np.deg2rad(63.43), 0, np.deg2rad(63.43)),
        image_format: str = "PNG",
        background_color: tuple = (0.0, 0.0, 0.0),
        frame_end: int = 1000,
        resolution_x: int = 1080,
        resolution_y: int = 720,
    ):
        """ """
        if anaglyph:
            bpy.data.scenes["Scene"].render.use_multiview = True
            if cyan:
                bpy.context.scene.render.image_settings.views_format = "STEREO_3D"

        # bpy.data.scenes['Scene'].render.use_raytrace = False
        bpy.data.objects["Camera"].location = camera_location
        bpy.data.objects["Camera"].rotation_euler = camera_tuple
        bpy.context.scene.render.image_settings.file_format = image_format
        world = bpy.data.worlds[0]
        world.use_nodes = True
        bg = world.node_tree.nodes["Background"]
        bg.inputs[0].default_value[:3] = background_color

        bpy.data.scenes["Scene"].frame_end = frame_end
        bpy.context.scene.render.resolution_x = resolution_x
        bpy.context.scene.render.resolution_y = resolution_y
        bpy.context.scene.render.resolution_percentage = 100

    def render_frame(self, i: int, scalar: float = 7.5e7):
        """
        """
        vs = self.positions[:, i, :] / scalar
        cs = plt.cm.inferno(temp[:, i, 0])[:, :3]
        c.draw(vs, None, cs)
        bpy.context.scene.frame_current = i
        bpy.ops.point_cloud_visualizer.render()

    def render(self):
        """
        """
        for i in tqmd.tqdm(range(positions.shape[1])):
            self.render_frame(i)

import bpy
import numpy as np
import matplotlib.pyplot as plt
from space_view3d_point_cloud_visualizer import PCVControl, PCV_OT_render
import os

positions = np.load(
    "../GI_vis_assets/new_data/positions_x1Downsample_pos.npy", mmap_mode="r"
)
temp = np.load("../GI_vis_assets/new_data/positions_x1Downsample_T.npy", mmap_mode="r")


def log_normalize(temp, T_min=1300, T_max=1e4):
    """
    Normalize a temperature array

    Args:

        Temperature in eV
    """
    T_ceiling = np.copy(temp) * 11604.0
    T_ceiling[np.where(T_ceiling > T_max)] = T_max
    T_ceiling[np.where(T_ceiling < T_min)] = T_min
    log_T_ceiling = np.log10(T_ceiling) - np.log10(T_min)
    log_T_ceiling_norm = log_T_ceiling / (np.log10(T_max) - np.log10(T_min))
    return log_T_ceiling_norm


def set_render_settings(anaglyph=False, cyan=False):
    """ """
    if anaglyph:
        bpy.data.scenes["Scene"].render.use_multiview = True
        if cyan:
            bpy.context.scene.render.image_settings.views_format = "STEREO_3D"

    # bpy.data.scenes['Scene'].render.use_raytrace = False
    bpy.data.objects["Camera"].location = (40, -20, 20)
    bpy.data.objects["Camera"].rotation_euler = (
        np.deg2rad(63.43),
        0,
        np.deg2rad(63.43),
    )
    bpy.context.scene.render.image_settings.file_format = "PNG"
    world = bpy.data.worlds[0]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value[:3] = (0.0, 0.0, 0.0)

    bpy.data.scenes["Scene"].frame_end = 1000
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 720
    bpy.context.scene.render.resolution_percentage = 100


def main(i):
    vs = positions[:, i, :] / 7.5e7
    cs = plt.cm.inferno(temp[:, i, 0])[:, :3]
    c.draw(vs, None, cs)
    bpy.context.scene.frame_current = i
    bpy.ops.point_cloud_visualizer.render()


if __name__ == "__main__":

    bpy.ops.wm.save_as_mainfile(filepath="untitled.blend")

    o = bpy.context.active_object
    c = PCVControl(o)
    pcv = bpy.context.object.point_cloud_visualizer
    pcv.render_path = os.path.join(os.getcwd(), "render/####")
    pcv.render_point_size = 4
    pcv.alpha_radius = 0.75
    set_render_settings()
    for i in np.arange(positions.shape[1]):
        vs = positions[:, i, :] / 7.5e7
        cs = plt.cm.inferno(log_normalize(temp[:, i, 0]))[:, :3]
        c.draw(vs, None, cs)
        bpy.ops.point_cloud_visualizer.render()
        bpy.context.scene.frame_current += 1

    os.remove("untitled.blend")

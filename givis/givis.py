import os
import sys
import argparse

import glob
import tqdm
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as mticker
from matplotlib.ticker import LogFormatter

try:
    import bpy
    from mathutils import *
    from math import *
except ImportError:
    print(
        "Module 'bpy' could not be imported. This probably means you are not using Blender to run this script."
    )
    sys.exit(1)


class Visualization:
    """ """

    def __init__(
        self,
        pos_file,
        var_file,
        output,
        mp=False,
        cores=4,
        color_bins=100,
        color_map=plt.cm.inferno,
        x_res=1920,
        y_res=1080,
        cut=False,
    ):
        """ """
        self.color_bins = color_bins
        self.color_map = color_map
        self.mp = mp
        self.cores = cores
        self.x_res = x_res
        self.y_res = y_res
        self.positions = np.load(pos_file, mmap_mode="r")
        self.variable = np.load(var_file, mmap_mode="r")
        self.cmap = self.color_map(np.linspace(0, 1, self.color_bins))
        self.output = output
        self.cut = cut

    def log_normalize(self, temp, T_min=100, T_max=6e3):
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

    def set_render_settings(self, anaglyph=True, cyan=False):
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
        bpy.data.worlds["World"].color = (0, 0, 0)
        bpy.data.scenes["Scene"].frame_end = 1000
        bpy.context.scene.render.resolution_x = self.x_res
        bpy.context.scene.render.resolution_y = self.y_res
        bpy.context.scene.render.resolution_percentage = 100

    def log_normalize_P(self, temp, T_min=1e8, T_max=5e12):
        """
        Normalize a temperature array

        Args:

            Temperature in eV
        """
        T_ceiling = np.copy(temp)
        T_ceiling[np.where(T_ceiling > T_max)] = T_max
        T_ceiling[np.where(T_ceiling < T_min)] = T_min
        log_T_ceiling = np.log10(T_ceiling) - np.log10(T_min)
        log_T_ceiling_norm = log_T_ceiling / (np.log10(T_max) - np.log10(T_min))
        return log_T_ceiling_norm

    def bin_data(self, pos, temp):
        """
        Bin data into separate color bins

        Arguments:
        ---------
            pos: (np.array)
                Position array of the particles
            temp: (np.array)
                Temperature array of the particles
            bins: (int)
                Number of bins

        Returns:
        --------
        """
        log_norm = self.log_normalize(temp)
        counts, bins = np.histogram(log_norm, bins=self.color_bins)
        idx = np.where(counts > 0)[0]
        dig = np.digitize(x=log_norm, bins=bins) - 1
        dig[dig == dig.max()] = dig.max() - 1
        particle_sets = []

        for d in np.sort(np.unique(dig)):
            particle_sets.append(pos[np.where(d == dig)[0], :])

        return particle_sets, idx

    def add_particle_system(self, name, pos=(0, 0, 0)):
        """ """
        bpy.ops.mesh.primitive_cube_add(location=pos, radius=10.0)
        bpy.context.selected_objects[0].name = name
        bpy.data.objects[name].modifiers.new("part", "PARTICLE_SYSTEM")
        bpy.context.scene.update()

    def set_particle_settings(self, data, obj_name, i=0):
        """ """
        obj = bpy.data.objects[obj_name]
        part_set = bpy.data.particles["ParticleSettings"]
        part_set.frame_start = 0
        part_set.frame_end = 0
        part_set.lifetime = 1000
        part_set.mass = 0
        part_set.count = data.shape[0]
        part_set.use_render_emitter = False
        part_set.name = str(i).zfill(4)
        part_set.material_slot = str(i).zfill(4)
        part = obj.particle_systems[0]
        part.seed += 1
        part.seed -= 1
        part.settings = part_set

    def clear_scene(self):
        """ """
        for o in bpy.data.objects:
            if o.type == "MESH" and o.name != "plane":
                # Changed from bpy.context.scene.objects.unlink(o)
                bpy.context.scene.collection.objects.unlink(o)
                bpy.data.objects.remove(o)

        for block in bpy.data.meshes:
            if block.name != "plane":
                block.user_clear()
                bpy.data.meshes.remove(block)

        for block in bpy.data.materials:
            if block.name != "plane":
                block.user_clear()
                bpy.data.materials.remove(block)

        for block in bpy.data.textures:
            block.user_clear()
            bpy.data.textures.remove(block)

    def render_frame(self, filename):
        """ """
        self.set_filename(filename)
        bpy.context.scene.update()
        bpy.ops.render.render(write_still=True)

    def set_filename(self, filename):
        """ """
        bpy.context.scene.render.filepath = os.path.join(self.output, filename)

    def set_material_settings(
        self,
        obj_name,
        i=0,
        halo_size=0.04,
        color=(255.0 / 255.0, 88.0 / 255.0, 0.0 / 255.0),
    ):
        obj = bpy.data.objects[obj_name]
        bpy.data.materials.new(str(i).zfill(4))
        m = bpy.data.materials[str(i).zfill(4)]
        m.type = "HALO"
        m.alpha = 1.0
        m.diffuse_color = color
        m.halo.size = halo_size
        m.halo.hardness = 127
        obj.data.materials.append(m)

    def main_properties(self, i):
        """ """
        data = self.positions[:, i, :]
        temp = self.variable[:, i, 0]

        if self.cut:
            idx = data[:, 2] < 0
            data = data[idx]
            temp = temp[idx]

        sets, idx = self.bin_data(data, temp)
        obj_list = []

        bpy.context.scene.frame_set(i + 1)

        for j, s in enumerate(sets):
            obj_name = str(j).zfill(4)
            obj_list.append(obj_name)
            self.add_particle_system(obj_name)
            self.set_material_settings(
                obj_name, i=j, halo_size=0.1, color=self.cmap[j][:3]
            )
            self.set_particle_settings(s[:, :3] / 7.5e7, obj_name, i=j)

        bpy.context.scene.update()

        for j, o in enumerate(obj_list):
            pos = sets[j]
            obj = bpy.data.objects[o]
            p = obj.particle_systems[0].particles
            p.foreach_set("location", pos[:, :3].ravel() / 7.5e7)

        bpy.context.scene.frame_set(i + 2)
        self.render_frame("{}.png".format(str(i).zfill(4)))
        self.clear_scene()

    def render(self):
        """ """
        self.set_render_settings(anaglyph=False, cyan=False)
        self.clear_scene()

        for i in tqdm.tqdm(np.arange(self.positions.shape[1])):
            self.main_properties(i)


"""






"""


class Colorbar:
    """ """

    def __init__(
        self,
        x_res=1920,
        y_res=1080,
        dpi=300,
        colormap=plt.cm.inferno,
        variable="temperature",
    ):
        self.x_res = x_res
        self.y_res = y_res
        self.dpi = dpi
        self.colormap = colormap
        self.variable = variable

        self.range = {
            "pressure": np.logspace(8, 12, 20),
            "temperature": np.logspace(2, 3.778, 20),
        }

    def set_colorbar(self):
        """ """
        figsize = (float(self.x_res) / self.dpi, float(self.y_res) / self.dpi)
        print(figsize)
        plt.style.use("dark_background")
        fig, ax = plt.subplots(figsize=figsize, dpi=self.dpi)

        s = plt.scatter(
            np.arange(20),
            np.arange(20),
            c=self.range[self.variable],
            cmap=self.colormap,
            norm=colors.LogNorm(),
        )

        f = mticker.ScalarFormatter(useOffset=False, useMathText=True)
        g = lambda x, pos: "${}$".format(f._formatSciNotation("%1.10e" % x))
        fmt = mticker.FuncFormatter(g)
        cbar = plt.colorbar(s, ax=ax, format=fmt)
        cbar.ax.tick_params(labelsize="large", labelcolor="white", pad=5)
        cbar.set_label(
            r"Temperature (K)",
            rotation=270,
            labelpad=22.0,
            fontsize=18,
            color="white",
            fontweight="heavy",
        )
        ax.remove()
        fig.subplots_adjust(0, 0.025, 1.01, 0.975)
        fig.savefig("cbar.png", transparent=False, dpi=self.dpi)

    def apply_colorbar(self):
        images = glob.glob("renders/*png")
        cbar = Image.open("cbar.png")
        for img_path in images:
            scene = Image.open(img_path)
            scene.paste(cbar, (0, 0), cbar)
            scene.save(img_path, "PNG")


"""
Validators
"""


def is_path(path):
    """ """
    if not os.path.exists(path):
        raise argparse.ArgumentTypeError("{} is an invalid path".format(path))
    return path


def make_path(path):
    """ """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def is_variable(var):
    """ """
    var = var.lower()
    if var not in ["temperature", "pressure", "t", "p"]:
        raise argparse.ArgumentTypeError("{} is an invalid variable type".format(path))
    return var


def split_res(res):
    """ """
    res = res.lower()
    x, y = res.split("x")
    return int(x), int(y)


def find_var(path, var="P"):
    """ """
    return glob.glob(os.path.join(path, "*_" + var + ".npy"))[0]


def set_output(path):
    """ """
    output = os.path.join(os.path.dirname(os.path.dirname(path)), "render")
    if not os.path.exists(output):
        os.makedirs(output)
    return output


# CLI
prog_name = "Giant Impact Visualization Tool"
if "--" not in sys.argv:
    print(
        prog_name
        + "No '--' found in command line arguments. '--' is needed to pass arguments to this script."
    )
    sys.exit(1)

# Parse arguments
arguments = sys.argv  # [sys.argv.index("--") + 1 :]

parser = argparse.ArgumentParser(description="Create captions")
parser.add_argument(
    "--data_path",
    "-p",
    type=is_path,
    default="/Users/Projects/givis/assets/",
    help="Path to the data folder",
)
parser.add_argument("--variable", "-v", type=is_variable, default="P", help="Variable")
parser.add_argument(
    "--size", "-s", default="640x320", help="Resolution size of the render"
)
parser.add_argument(
    "--colorbar", "-cb", default=False, type=bool, help="Add a colorbar to the frame"
)
parser.add_argument("--bins", "-b", default=100, type=int, help="Number of color bins")
parser.add_argument(
    "--multiprocessing", "-mp", type=str, default=False, help="Use multiprocessing"
)
parser.add_argument(
    "--cores", "-c", type=int, default=2, help="Number of cores used in multiprocessing"
)
parser.add_argument("--cut", "-cut", type=bool, default=False, help="Sliced view")

args = parser.parse_args(arguments)
data_path = args.data_path
variable = args.variable
size = args.size
colorbar = args.colorbar
color_bins = args.bins
mp = args.multiprocessing
cores = args.cores
cut = args.cut

pos_file = find_var(data_path, "pos")
var_file = find_var(data_path, variable[0].upper())
output = set_output(data_path)
x_res, y_res = split_res(size)


if __name__ == "__main__":
    # Set the rendering settings
    vis = Visualization(
        pos_file=pos_file,
        var_file=var_file,
        output=output,
        x_res=x_res,
        y_res=y_res,
        mp=mp,
        cores=cores,
        color_bins=color_bins,
        cut=cut,
    )
    vis.render()

    # Add a color bar to the frames
    if colorbar:
        cb = Colorbar()
        cb.set_colorbar()
        cb.apply_colorbar()

    # Frames to video

from Aslide.aslide import Aslide
from Aslide.deepzoom import ADeepZoomGenerator
import math


# path = '/home/stimage/Development/DATA/TEST_DATA/TC18056060.kfb'
path = '/home/stimage/Development/DATA/TEST_DATA/2018-03-22-11_31_24.tif'

slice = Aslide(path)
l_dimensions = slice.level_dimensions
print("l_dimensions")
print(l_dimensions)
l0_offset = (0, 0)

l0_dimensions = l_dimensions[0]
print("l0_dimensions")
print(l0_dimensions)

z_size = l0_dimensions
z_dimensions = [z_size]

while z_size[0] > 1 or z_size[1] > 1:
    z_size = tuple(max(1, int(z / 2)) for z in z_size)
    z_dimensions.append(z_size)

print("z_dimensions")
print(z_dimensions)
z_dimensions = tuple(reversed(z_dimensions))
print("z_dimensions_reversed")
print(z_dimensions)

z_t_downsample = 254
tiles = lambda z_lim: int(z_lim / z_t_downsample)
t_dimensions = tuple((tiles(z_w), tiles(z_h)) for z_w, z_h in z_dimensions)
print("t_dimensions")
print(t_dimensions)

dz_levels = len(z_dimensions)

l0_z_downsamples = tuple(2 ** (dz_levels - dz_level - 1) for dz_level in range(dz_levels))
print("l0_z_downsamples")
print(l0_z_downsamples)

slide_from_dz_level = tuple(slice.get_best_level_for_downsample(d) for d in l0_z_downsamples)
print("slide_from_dz_level")
print(slide_from_dz_level)

l0_l_downsamples = slice.level_downsamples
print("l0_l_downsamples")
print(l0_l_downsamples)

l_z_downsamples = tuple(l0_z_downsamples[dz_level] / l0_l_downsamples[slide_from_dz_level[dz_level]] for dz_level in range(dz_levels))
print("l_z_downsamples")
print(l_z_downsamples)


def l0_from_l(slide_level, l):
    return l0_l_downsamples[slide_level] * l

def l_from_z(dz_level, z):
    return l_z_downsamples[dz_level] * z

def z_from_t(t):
    return z_t_downsample * t


dz_level = 10
z_overlap = 1
t_location = (3, 3)

slide_level = slide_from_dz_level[dz_level]
print(slide_level)

t, t_lim = t_dimensions[dz_level]
print(t, t_lim)

print(t_location, t_dimensions[dz_level])
z_overlap_tl = tuple(z_overlap * int(t != 0) for t in t_location)
z_overlap_br = tuple(z_overlap * int(t != t_lim - 1) for t, t_lim in zip(t_location, t_dimensions[dz_level]))
print("z_overlap_tl, z_overlap_br")
print(z_overlap_tl, z_overlap_br)

z_size = tuple(min(z_t_downsample, z_lim - z_t_downsample * t) + z_tl + z_br for t, z_lim, z_tl, z_br in zip(t_location, z_dimensions[dz_level], z_overlap_tl, z_overlap_br))
print("z_size")
print(z_size)

# Obtain the region coordinates
z_location = [z_from_t(t) for t in t_location]
l_location = [l_from_z(dz_level, z - z_tl) for z, z_tl in zip(z_location, z_overlap_tl)]
print("l_location")
print(l_location)

# Round location down and size up, and add offset of active area
l0_location = tuple(int(l0_from_l(slide_level, l) + l0_off) for l, l0_off in zip(l_location, l0_offset))
print("l0_location")
print(l0_location)

l_size = tuple(int(min(math.ceil(l_from_z(dz_level, dz)), l_lim - math.ceil(l))) for l, dz, l_lim in zip(l_location, z_size, l_dimensions[slide_level]))

# Return read_region() parameters plus tile size for final scaling
# print((l0_location, slide_level, l_size), z_size)
# print(l_dimensions[slide_level])
# print(t_dimensions[dz_level])






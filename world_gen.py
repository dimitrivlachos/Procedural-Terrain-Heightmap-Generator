'''
File: world_gen.py
Author: Dimitrios Vlachos (dimitri.j.vlachos@gmail.com)
Date: 12th July 2023
Github: https://github.com/dimitrivlachos/Procedural-Terrain-Heightmap-Generator
Description: 
    This program is inteneded to generate a heightmap for terrain using the Perlin Noise algorithm.
    The method used is based on Minecraft's terrain generation algorithm, using a stack of layers
    of Perlin Noise with different frequencies and amplitudes. The result is a heightmap that can
    be used to generate a 3D terrain.

    This terrain heightmap is then intended to be imported into ARC-GIS to generate a 3D terrain.
    However, this should be usable for any other 3D terrain generation needs, so long as a
    greyscale heightmap is acceptable input.

Sources:
    Numpy implementation of Perlin Noise:
    https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html

    Exellent article on Minecraft's terrain generation algorithm:
    https://www.alanzucconi.com/2022/06/05/minecraft-world-generation/
'''

import noise.perlin_noise as pn

class Terrain:
    '''
    A class to represent a terrain heightmap.

    Attributes
    ----------
    size : tuple of ints
        The size of the heightmap in pixels. (x, y)
    seed : int
        The seed used to generate the heightmap.

    Methods
    -------

    '''

    def __init__(self, size, seed):
        '''
        Constructs all the necessary attributes for the terrain object.

        Parameters
        ----------
        size : tuple of ints
            The size of the heightmap in pixels. (x, y)
        seed : int
            The seed used to generate the heightmap.
        '''

        # Check that the size is a tuple of ints
        if not isinstance(size, tuple):
            raise TypeError('Size must be a tuple of ints.')
        if not isinstance(size[0], int) or not isinstance(size[1], int):
            raise TypeError('Size must be a tuple of ints.')
        
        # Check that the size of size is 2
        if len(size) != 2:
            raise ValueError('Size must be a tuple of length 2. (x, y)')
        
        # Check that the seed is an int
        if not isinstance(seed, int):
            raise TypeError('Seed must be an int.')

        # If all checks pass, set the attributes
        self.size = size
        self.seed = seed
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

import numpy as np
import functions.perlin_noise as pn
import functions.cellular_automata as ca

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

    def __init__(self, seed, start_size = (4, 4)):
        '''
        Constructs all the necessary attributes for the terrain object.

        Parameters
        ----------
        seed : int
            The seed used to generate the heightmap.
        size : tuple of ints
            The size of the initial seed-map. This will be 4096 times smaller than the final heightmap.
            Default is (4, 4) which will result in a 4x4 seed-map and a 16384x16384 pixel heightmap.
        '''
        # Check that the seed is an int
        if not isinstance(seed, int):
            raise TypeError('Seed must be an int.')
        
        # Check that the size is a tuple of ints
        if not isinstance(start_size, tuple):
            raise TypeError('Size must be a tuple of ints.')
        if not isinstance(start_size[0], int) or not isinstance(start_size[1], int):
            raise TypeError('Size must be a tuple of ints.')
        
        # Check that the size of size is 2
        if len(start_size) != 2:
            raise ValueError('Size must be a tuple of length 2. (x, y)')

        # If all checks pass, set the attributes
        self.seed = seed
        self.start_size = start_size
        self.size = start_size # This will be updated as the heightmap is generated
        self.is_generated = False
        self.heightmap = None

        # Instantiate the random number generator
        self.rng = np.random.default_rng(seed = self.seed)

    def __str__(self):
        '''
        Returns a string representation of the terrain object.

        Parameters
        ----------
        None

        Returns
        -------
        string : str
            A string representation of the terrain object.
        '''
        return f'Terrain object with seed {self.seed} and start size {self.start_size}.'

    def __zoom(self, heightmap, zoom_factor = 2):
        '''
        'Zooms' in on the terrain object by the given factor (default is 2).
        This is done through the usage of cellular automata.

        Parameters
        ----------
        heightmap : numpy array
            The heightmap to zoom in on.
        zoom_factor : int
            The factor by which to zoom in on the terrain object. Default is 2.

        Returns
        -------
        zoomed_heightmap : numpy array
            The zoomed in heightmap.
        '''
        # Check that the zoom factor is an int
        if not isinstance(zoom_factor, int):
            raise TypeError('Zoom factor must be an int.')
        
        # Check that the zoom factor is greater than 0
        if zoom_factor < 1:
            raise ValueError('Zoom factor must be greater than 0.')

        # Increase the size of the heightmap by the zoom factor
        zoomed_heightmap = np.kron(heightmap, np.ones((zoom_factor, zoom_factor)))

        # Increase the tracked size of the heightmap
        self.size = (self.size[0] * zoom_factor, self.size[1] * zoom_factor)

        # Return the zoomed heightmap
        return zoomed_heightmap
    
    def __add_island(self, heightmap):
        '''
        Uses cellular automata to add an island to the heightmap. Connecting existing islands together
        and eroding the edges of the island.

        Parameters
        ----------
        heightmap : numpy array
            The heightmap to add an island to.

        Returns
        -------
        island_heightmap : numpy array
            The heightmap with an island added to it.
        '''

        # Initialize the island layer


    def generate(self):
        '''
        Generates the heightmap for the terrain object.

        Parameters
        ----------
        None

        Returns
        -------
        heightmap : numpy array
            The heightmap for the terrain object.
        '''

        # Initialize the seed map / island layer
        island_layer = np.zeros(self.start_size, dtype = int)

        print(island_layer)
        
        # Randomly set 1/10 of the pixels to 1
        indices_to_flip = self.rng.random(island_layer.shape) < 0.1
        island_layer[indices_to_flip] = 1

        print(island_layer)

        # Zoom in on the island layer
        # This takes the island layer from 4x4 to 8x8 (by default)
        island_layer = self.__zoom(island_layer)

        print(island_layer)

        # Apply cellular automata to the island layer
        #for i in range(5):
        island_layer = ca.cellular_automata(island_layer, ca.game_of_life)

        print('Cellular\n', island_layer)


# Test code
if __name__ == '__main__':
    terraintest = Terrain(0)
    terraintest.generate()
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
import numpy as np

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

        # Return the zoomed heightmap
        return zoomed_heightmap
    
    def __live_or_die(self, cell, neighbours):
        '''
        Determines whether a cell lives or dies based on the number of live neighbours.

        Parameters
        ----------
        cell : int
            The value of the cell
        neighbours : int
            The number of live neighbours of the cell

        Returns
        -------
        cell : int
            The value of the cell after the cellular automata rules have been applied.
        '''
        # If the cell is alive
        if cell == 1:
            # If the cell has less than 2 live neighbours, it dies
            if neighbours < 2:
                cell = 0
            # If the cell has more than 3 live neighbours, it dies
            elif neighbours > 3:
                cell = 0
            # If the cell has 2 or 3 live neighbours, it lives
            else:
                cell = 1

        # If the cell is dead
        else:
            # If the cell has exactly 3 live neighbours, it lives
            if neighbours == 3:
                cell = 1

        # Return the cell
        return cell
    
    def __cellular_automata(self, heightmap):
        '''
        Applies cellular automata to the heightmap.

        Parameters
        ----------
        heightmap : numpy array
            The heightmap to apply cellular automata to.

        Returns
        -------
        heightmap : numpy array
            The heightmap after cellular automata has been applied.
        '''
        # Create a copy of the heightmap
        heightmap_copy = heightmap.copy()

        # Iterate over the heightmap
        for x in range(heightmap.shape[0]):
            for y in range(heightmap.shape[1]):
                # Get the number of live neighbours
                neighbours = self.__get_neighbours(heightmap, x, y)

                # Determine whether the cell lives or dies
                heightmap_copy[x, y] = self.__live_or_die(heightmap[x, y], neighbours)

        # Return the heightmap
        return heightmap_copy
    
    def __get_neighbours(self, heightmap, x, y):
        '''
        Gets the neighbours of a given cell.

        Parameters
        ----------
        heightmap : numpy array
            The heightmap to get the neighbours from.
        x : int
            The x coordinate of the cell.
        y : int
            The y coordinate of the cell.

        Returns
        -------
        neighbours : int
            The number of live neighbours of the cell.
        '''
        # Initialize the number of neighbours
        neighbours = 0

        # Iterate over the neighbours
        for i in range(-1, 2):
            for j in range(-1, 2):
                # If the neighbour is the cell itself, skip it
                if i == 0 and j == 0:
                    continue

                # If the neighbour is outside the heightmap, skip it
                if x + i < 0 or x + i >= heightmap.shape[0] or y + j < 0 or y + j >= heightmap.shape[1]:
                    continue

                # If the neighbour is alive, increase the number of neighbours
                if heightmap[x + i, y + j] == 1:
                    neighbours += 1

        # Return the number of neighbours
        return neighbours

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
        island_layer = self.__zoom(island_layer)

        print(island_layer)

        # Apply cellular automata to the island layer
        #for i in range(5):
        island_layer = self.__cellular_automata(island_layer)

        print('Cellular\n', island_layer)


# Test code
if __name__ == '__main__':
    terraintest = Terrain(0)
    terraintest.generate()
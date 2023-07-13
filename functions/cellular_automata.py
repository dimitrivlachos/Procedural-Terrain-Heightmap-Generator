'''
File: cellular_automata.py
Author: Dimitrios Vlachos (dimitri.j.vlachos@gmail.com)
Date: 13th July 2023
Github: https://github.com/dimitrivlachos/Procedural-Terrain-Heightmap-Generator

Description:
    These functions are used to apply cellular automata algorithms to a heightmap.
'''

def cellular_automata(heightmap, algorithm):
    '''
    Applies cellular automata to the heightmap.

    Parameters
    ----------
    heightmap : numpy array
        The heightmap to apply cellular automata to.
    algorithm : function
        The algorithm to use for cellular automata. This should be a function that takes two arguments:
        cell : int
            The value of the cell
        neighbours : int
            The number of live neighbours of the cell
        and returns the value of the cell after the cellular automata rules have been applied.

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
            neighbours = get_neighbours(heightmap, x, y)

            # Determine whether the cell lives or dies
            heightmap_copy[x, y] = algorithm(heightmap[x, y], neighbours)

    # Return the heightmap
    return heightmap_copy

def get_neighbours(heightmap, x, y):
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


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Cellular automata algorithms

def game_of_life(cell, neighbours):
        '''      
        Determines whether a cell lives or dies based on the number of live neighbours.
        This is the algorithm used by Conway's Game of Life.

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
'''
File: cellular_automata.py
Author: Dimitrios Vlachos (dimitri.j.vlachos@gmail.com)
Date: 13th July 2023
Github: https://github.com/dimitrivlachos/Procedural-Terrain-Heightmap-Generator

Description:
    These functions are used to apply cellular automata algorithms to a heightmap.
'''

def cellular_automata(heightmap, algorithm, rng = None):
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
            heightmap_copy[x, y] = algorithm(heightmap[x, y], neighbours, rng)

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

def game_of_life(cell, neighbours, rng = None):
    '''      
    One of the cellular automata algorithms that can be used to generate terrain.
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

def brians_brain(cell, neighbours, rng = None):
        '''      
        One of the cellular automata algorithms that can be used to generate terrain.
        Determines whether a cell lives or dies based on the number of live neighbours.
        This is the algorithm used by Brian's Brain.

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
            # The cell dies
            cell = 0

        # If the cell is dead
        else:
            # If the cell has 6, 7, 8 live neighbours, it lives
            if neighbours >= 6:
                cell = 1

        # Return the cell
        return cell

def add_island(cell, neighbours, rng = None):
    '''
    One of the cellular automata algorithms that can be used to generate terrain.
    Determines whether a cell lives or dies based on the number of live neighbours.
    This is a custom algorithm that connects islands together and erodes the edges.

    Parameters
    ----------
    cell : int
        The value of the cell
    neighbours : int
        The number of live neighbours of the cell
    rng : numpy random generator
        The random number generator to use.

    Returns
    -------
    cell : int
        The value of the cell after the cellular automata rules have been applied.
    '''

    # Check if the random number generator is None
    if rng is None:
        raise ValueError("Random number generator is required for this algorithm. The random number generator cannot be None.")

    # If the cell is alive
    if cell == 1:
        # The cell has a chance to die relative to the number of dead neighbours
        chance_to_die = 1 - ((neighbours + 8) / 24)

        if rng.random() < chance_to_die:
            cell = 0

    # If the cell is dead
    else:
        # The cell has a chance to live relative to the number of live neighbours
        chance_to_live = (neighbours + 8) / 24

        if rng.random() < chance_to_live:
            cell = 1

    # Return the cell
    return cell
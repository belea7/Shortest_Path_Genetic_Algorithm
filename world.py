"""
Includes class representing the world of the robot.
"""
from random import sample
from chromosome import Chromosome


class World:
    """
    Class representing a world which the robot has to explore.
    """
    def __init__(self, size, obstacles):
        """
        Constructor for class world.
        """
        # Create grid of the world
        self.size = size
        self.grid = []
        for row in range(size):
            self.grid.append([])
            for col in range(size):
                self.grid[row].append(False)

        # Add the obstacles
        self.obstaclesList = []

        # Choose start and destination points
        self.start = None
        self.dest = None
        self.choose_special_cells(obstacles)
        self.manhattanDistance = Chromosome.manhattan_distance(self.start, self.dest)

    def choose_special_cells(self, obstacles):
        """
        Adds obstacles to the map, chooses start and destination points.
        :returns: None
        """
        cells = []
        for y in range(self.size):
            for x in range(self.size):
                cells.append((y, x))

        # Add obstacles to the map
        self.obstaclesList.extend(sample(cells, obstacles))
        for cell in self.obstaclesList:
            y, x = cell
            self.grid[y][x] = True

        # Choose start and destination points
        cells = set(cells) - set(self.obstaclesList)
        points = sample(cells, 2)
        self.start = points[0]
        self.dest = points[1]

    def changeObstacles(self, number):
        """
        Adds new obstacles to the grid.
        :param number: Total number of obstacles required.
        :returns: None
        """
        # Create a list of all cells
        cells = []
        for y in range(self.size):
            for x in range(self.size):
                cells.append((y, x))

        # Remove the start, destination and obstacles points
        cells = set(cells) - set(self.obstaclesList)
        cells.remove(self.start)
        cells.remove(self.dest)

        # Randomly add obstacles to the grid
        new = number - len(self.obstaclesList)
        newCells = sample(cells, new)
        for y, x in newCells:
            self.grid[y][x] = True
        self.obstaclesList.extend(newCells)

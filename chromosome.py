"""
Includes the Chromosome class.
"""
from random import choice, randint
import constants as const


class Chromosome:
    """
    Represents a chromosome in the population.
    """
    def __init__(self, world, path=None, size=0):
        """
        Constructor for class chromosome.
        If a path is given - set this path to the chromosome.
        If not given a path - randomly create a path.
        """
        self.world = world
        self.path = path if path else self.create_path(size)        # The path the chromosome represents
        self.pathLength = 0                                         # Length of the path
        self.destReached = False                                    # Is destination reached
        self.history = []                                           # Visited cells by the path
        self.obstacles = False                                      # Does the path go through obstacles
        self.fitness = self.fitness_func()                          # Fitness value of the chromosome

    def create_path(self, size):
        """
        Creates a random path.
        :returns: the path of the chromosome (list of direction)
        """
        path = []
        for _ in range(size):
            path.append(choice(const.DIRECTIONS))
        return path

    def fitness_func(self):
        """
        Calculate fitness as sum of the fallowing values:
            1. Length of the path (or path to destination).
            2. Number of the cells revisited.
            3. Number of obstacles * 10
            4. Number of opposite directions.
        :returns: the fitness value of the chromosome
        """
        current, revisitedCells, obstacles = self.walk()
        fitness = self.pathLength
        fitness += revisitedCells * const.REVISITED_CELL_PENALTY
        fitness += obstacles * const.OBSTACLE_PENALTY
        fitness += self.count_opposite_directions() * const.OPPOSITE_DIRECTIONS_PENALTY
        if not self.destReached:
            fitness += self.manhattan_distance(current, self.world.dest)
        return fitness

    def walk(self):
        """
        1. Checks if destination is reached.
        2. If reached - returns the number of steps to destination.
        3. Counts obstacles visited by the path.
        4. Counts number of cells out of the grid boundaries.
        :returns: the current cell (or the destination cell if reached), number of cells revisited
                  and number of obstacles visited.
        """
        dest = self.world.dest
        current = self.world.start
        revisitedCells = 0
        obstacles = 0
        self.history = [self.world.start]
        for index in range(len(self.path)):
            # Update the current position
            current = self.update_coordinates(current, index)

            # Check if path exits the bounds of the grid
            currentY, currentX = current
            while currentX >= self.world.size or currentX < 0 or currentY >= self.world.size or currentY < 0:
                current = self.fix_direction(current, index)
                currentY, currentX = current

            # Check if any cell is revisited
            if current in self.history:
                revisitedCells += 1
            self.history.append(current)

            # Check if destination is reached
            if currentY == dest[0] and currentX == dest[1]:
                self.destReached = True
                break

            # Check if on obstacle
            if current in self.world.obstaclesList:
                obstacles += 1

        self.pathLength = len(self.history) - 1
        if obstacles > 0:
            self.obstacles = True
        return current, revisitedCells, obstacles

    def update_coordinates(self, current, index):
        """
        Updates the coordinates according to the direction.
        :param current: current coordinates
        :param index: index of the direction
        :return: new coordinates
        """
        currentY, currentX = current
        direction = self.path[index]
        if direction == "Up":
            currentY += 1
        elif direction == "Down":
            currentY -= 1
        elif direction == "Left":
            currentX -= 1
        else:
            currentX += 1
        return (currentY, currentX)

    def fix_direction(self, current, index):
        """
        Fixes direction in the path if it exits the boundaries of the grid.
        :param current: current coordinates
        :param index: index of the direction
        :returns: new coordinates
        """
        direction = self.path[index]
        currentY, currentX = current
        if direction == "Up":
            currentY -= 1
        elif direction == "Down":
            currentY += 1
        elif direction == "Left":
            currentX += 1
        else:
            currentX -= 1
        self.path[index] = choice([d for d in const.DIRECTIONS if d != direction])
        new = (currentY, currentX)
        return self.update_coordinates(new, index)

    def count_opposite_directions(self):
        """
        Count opposite directions.
        If number of opposite directions is high - the path may have redundant actions.
        :returns: sum of minimal number between "up" and "south" directions and "left" and "right" directions.
        """
        actualPath = self.path[:self.pathLength]
        upDown = min([actualPath.count("Up"), actualPath.count("Down")])
        rightLeft = min([actualPath.count("Right"), actualPath.count("Left")])
        return upDown + rightLeft

    def mutate(self):
        """
        Performs mutation on a chromosome.
        Randomly changes the direction in a random point in the path.
        :returns: None
        """
        index = randint(0, len(self.path)-1)
        self.path[index] = choice(const.DIRECTIONS)

    def __str__(self):
        """
        Creates a string representing the chromosome.
        :returns: None
        """
        string = "Path: " + " , ".join(self.path)
        string += "\nFitness: {}".format(self.fitness)
        if self.destReached:
            "\tDESTINATION REACHED"
        if self.obstacles:
            string += "\tBUT WITH OBSTACLES."
        if self.destReached and not self.obstacles:
            string += "\t\nPATH FOUND.\n"
        else:
            string += "\t\nPATH NOT REACHED.\n"
        return string

    @staticmethod
    def manhattan_distance(p1, p2):
        """
        Calculates Manhattan Distance between 2 positions.
        :param: 2 positions coordinates
        :returns: manhattan distance
        """
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)

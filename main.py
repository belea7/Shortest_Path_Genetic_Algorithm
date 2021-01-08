"""
Runs the program with a list of parameters. Creates graphs and images.
"""
import argparse as arg
import tkinter as tk
import matplotlib.pyplot as plt

from world import World
from genetic_algorithm import GeneticSearchAlgorithm
import constants as const


def present_result(world, string):
    """
    Presents a view of the world, start and destination points, and the path found.
    :returns: None
    """
    root = tk.Tk()
    root.title("Maman 12 - Biological Computation - Lea Ben Zvi")

    # Set label and canvas of the window
    height = world.size * const.CELL_SIZE
    label = tk.Label(root)
    label.pack()
    label.config(text=string)
    canvas = tk.Canvas(root, height=height, width=height)
    canvas.pack()

    # Create the cell objects in the GUI
    for row in range(world.size):
        for col in range(world.size):
            if (row, col) == world.start:
                color = "green"
            elif (row, col) == world.dest:
                color = "red"
            elif world.grid[row][col]:
                color = "black"
            elif (row, col) in history:
                color = "yellow"
            else:
                color = "white"
            canvas.create_rectangle(row * const.CELL_SIZE,
                                    col * const.CELL_SIZE,
                                    (row + 1) * const.CELL_SIZE,
                                    (col + 1) * const.CELL_SIZE, fill=color)
    root.mainloop()


def create_graphs():
    """
    Creates the following graphs:
        1. Min fitness values over generations.
        2. Average fitness values over generations.
        3. Max fitness values over generations.
    :return: None
    """
    plt.figure(1, figsize=(15, 15))
    plt.subplots_adjust(hspace=0.5)

    # Create min graph
    plt.subplot(311, title="Fitness Min Values")
    plt.grid(True)
    plt.xlabel("Generations")
    plt.ylabel("Fitness min value")
    colorIndex = 0
    for conf in data.keys():
        gens = data[conf].keys()
        color = const.COLORS[colorIndex]
        colorIndex += 1
        minValues = [data[conf][gen]["min"] for gen in gens]
        plt.plot(gens, minValues, label=conf, color=color)
    plt.legend()

    # Create avg graph
    plt.subplot(312, title="Fitness Average Values")
    plt.grid(True)
    plt.xlabel("Generations")
    plt.ylabel("Fitness avg value")
    colorIndex = 0
    for conf in data.keys():
        gens = data[conf].keys()
        color = const.COLORS[colorIndex]
        colorIndex += 1
        avgs = [data[conf][gen]["avg"] for gen in gens]
        plt.plot(gens, avgs, label=conf, color=color)
    plt.legend()

    # Create max graph
    plt.subplot(313, title="Fitness Max Values")
    plt.grid(True)
    plt.xlabel("Generations")
    plt.ylabel("Fitness max value")
    colorIndex = 0
    for conf in data.keys():
        gens = data[conf].keys()
        color = const.COLORS[colorIndex]
        colorIndex += 1
        maxValues = [data[conf][gen]["max"] for gen in gens]
        plt.plot(gens, maxValues, label=conf, color=color)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # Handle arguments received by the program
    parser = arg.ArgumentParser(description="Create a grid world and find optimal path between two points.")
    parser.add_argument("-s", "--size", help="Size of the world. Can be a list separated by commas. Default={}"
                        .format(const.DEFAULT_WORLD_SIZE), default=const.DEFAULT_WORLD_SIZE, type=str)
    parser.add_argument("-o", "--obstacles", help="Number of obstacles. Can be a list separated by commas.  Default={}"
                        .format(const.DEFAULT_OBSTACLES), default=const.DEFAULT_OBSTACLES, type=str)
    parser.add_argument("-p", "--population", type=str,
                        help="Size of the population. Can be a list separated by commas. Default=world size * 1.5")
    parser.add_argument("-m", "--mutation", help="Mutation probability. Can be a list separated by commas. Default={}"
                        .format(const.DEFAULT_MUTATION_PROBABILITY), default=const.DEFAULT_MUTATION_PROBABILITY, type=str)
    parser.add_argument("-e", "--elite", help="Elite probability. Can be a list separated by commas. Default={}"
                        .format(const.DEFAULT_ELITE_PERCENTAGE), default=const.DEFAULT_ELITE_PERCENTAGE, type=str)
    parser.add_argument("-pp", "--parents", help="Parents percentage. Can be a list separated by commas. Default={}"
                        .format(const.DEFAULT_PARENTS_PERCENTAGE), default=const.DEFAULT_PARENTS_PERCENTAGE, type=str)
    args = vars(parser.parse_args())

    # Get lists of the arguments
    worldSizes = [int(x) for x in args["size"].split(",")]
    obstacleNumbers = [int(x) for x in args["obstacles"].split(",")]
    mutationProbabilities = [float(x) for x in args["mutation"].split(",")]
    elitePercentages = [float(x) for x in args["elite"].split(",")]
    parentsPercentages = [float(x) for x in args["parents"].split(",")]

    populationSizes = []
    populationGiven = False
    # If population sizes specified
    if args["population"]:
        populationGiven = True
        populationSizes = [int(x) for x in args["population"].split(",")]

    # Run the configurations
    configuration = 1
    data = {}
    for size in worldSizes:
        index = 0
        grid = World(size=size, obstacles=0)
        for obstacleNumber in obstacleNumbers:
            grid.changeObstacles(obstacleNumber)
            for mutationProbability in mutationProbabilities:
                for elitePercentage in elitePercentages:
                    for parentsPercentage in parentsPercentages:
                        # If population sizes not specified - set default size
                        if not populationGiven:
                            populationSizes = [size * const.POPULATION_FACTOR]
                        for populationSize in populationSizes:
                            # Run genetic algorithm on the world
                            string = ("Configuration #{0}: world_size={1}, number_of_obstacles={2}, population_size={3}"
                                      .format(configuration, size, obstacleNumber, populationSize))
                            if len(mutationProbabilities) > 1:
                                string += ", mutation_probability={}".format(mutationProbability)
                            if len(elitePercentages) > 1:
                                string += ", elite_percentage={}".format(elitePercentage)
                            if len(parentsPercentages) > 1:
                                string += ", parents_percentage={}".format(parentsPercentage)
                            print(string)
                            ga = GeneticSearchAlgorithm(grid, populationSize=populationSize,
                                                        mutationProbability=mutationProbability,
                                                        elitePercentage=elitePercentage,
                                                        parentPercentage=parentsPercentage)
                            configuration += 1
                            history = ga.start()

                            # Update the data dict
                            name = "size={0}_obstacles={1}_pop={2}".format(size, obstacleNumber, populationSize)
                            if len(mutationProbabilities) > 1:
                                name += "_mutation={}".format(mutationProbability)
                            if len(elitePercentages) > 1:
                                name += "_elite={}".format(elitePercentage)
                            if len(parentsPercentages) > 1:
                                name += "_parents={}".format(parentsPercentage)
                            data[name] = ga.data
                            present_result(grid, string)
    create_graphs()

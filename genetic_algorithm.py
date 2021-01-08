"""
Includes the Genetic Algorithm class.
"""
from random import choice, random
import numpy
import constants as const
from chromosome import Chromosome


class GeneticSearchAlgorithm:
    """
    Genetic algorithm
    """
    def __init__(self, world, populationSize, mutationProbability, elitePercentage, parentPercentage):
        """
        Constructor for GA class.
        :return:
        """
        # Parameters
        self.populationSize = int(populationSize)                       # Size of the population
        self.mutationProbability = mutationProbability                  # Probability for a mutation
        self.eliteSize = int(self.populationSize * elitePercentage)     # Size of the elite group
        self.parentSize = int(self.populationSize * parentPercentage)   # Size of the parents group

        self.world = world                          # The World object where the GA searches paths
        self.generation = 0                         # Generation of the GA
        self.sameFittestGenerations = 0             # How many generations the best chromosome hasn't changed
        self.samePopulationGenerations = 0          # How many generations the population's fitness values are equal
        self.chromosomeSize = self.world.size * 2   # Size of the chromosome
        self.population = None                      # The GA's population
        self.bestChromosome = None                  # The chromosome with the highest fitness value
        self.create_population()
        self.data = {}                              # Data about the fitness values in every generation
        self.update_data()

    def start(self):
        """
        Runs the GA:
            1. Print initial status of the population.
            2. Repeat until any of the stop conditions occurred.
                2.1 Create new generation of chromosomes.
                2.2 Perform selection process on the population.
                2.3 Print current status.
            3. Return the optimal path if found.

        The stop conditions:
            1. If the grid doesn't contain obstacles - optimal path was found - a chromosome whose fitness value is the
               Manhattan distance between the start and the destination points.
            2. The fittest chromosome hasn't changed for 150 of generations.
            3. All the chromosome in the population have the same fitness values for 50 generations.
        :returns: All the cells that were visited by the path.
        """
        # Print the initial status of the algorithm
        self.print_status()

        # Perform the steps of the GA while none of the stop conditions occurred.
        while self.sameFittestGenerations < const.SAME_FITTEST_MAX_GENERATIONS \
                and self.samePopulationGenerations < const.SAME_POPULATION_MAX_GENERATIONS:
            if len(self.world.obstaclesList) == 0 and self.bestChromosome.fitness == self.world.manhattanDistance:
                break

            # If all chromosomes in the population share the same fitness value - increase counter
            if len(set(x.fitness for x in self.population)) == 1:
                self.samePopulationGenerations += 1
            # Else - set counter to zero
            else:
                self.samePopulationGenerations = 0

            # Create a new generation of chromosomes and perform selection
            self.create_generation()
            self.selection()

            # Print status and update data dict
            self.print_status()
            self.update_data()

        # If a path that reaches destination was found - print it
        if self.bestChromosome.destReached and not self.bestChromosome.obstacles:
            length = self.bestChromosome.pathLength
            string = "Found best path from {0} to {1}".format(self.world.start, self.world.dest)
            string += "\n(Manhattan Distance: {})\n" \
                .format(Chromosome.manhattan_distance(self.world.start, self.world.dest))
            string += "{0} moves: {1}".format(length, " , ".join(self.bestChromosome.path[:length]))
            print(string)
        else:
            print("Path not found")
        return self.bestChromosome.history

    def create_generation(self):
        """
        Creates a new generation using crossovers and mutations.
        :return:
        """
        self.generation += 1
        # Choose parents using roulette selection
        parents = self.roulette_selection()

        # Perform crossovers between parents
        while parents:
            if len(parents) >= 2:
                parent1 = choice(parents)
                parents.remove(parent1)
                parent2 = choice(parents)
                parents.remove(parent2)
                self.population.extend(self.uniform_crossover(parent1, parent2))
            else:
                self.population.extend(parents)
                parents.clear()

        # Perform mutations in population - elite group doesn't change
        self.population = sorted(self.population, key=lambda x: x.fitness)[:self.populationSize]
        for chrom in self.population[self.eliteSize:]:
            if random() < self.mutationProbability:
                chrom.mutate()

        self.population = sorted(self.population, key=lambda x: x.fitness)[:self.populationSize]
        self.find_best_chromosome()

    def create_population(self):
        """
        Creates population of chromosomes (paths) and finds the fittest one.
        :returns: None
        """
        population = []
        for _ in range(self.populationSize):
            population.append(Chromosome(world=self.world, size=self.chromosomeSize))
        self.population = sorted(population, key=lambda x: x.fitness)
        self.find_best_chromosome()

    def roulette_selection(self):
        """
        Roulette wheel selection.
        To turn min values to max values - manhattan distance is divided by the fitness value.
        :returns: a list of parents
        """
        manhattan = self.world.manhattanDistance
        totalFitness = sum([manhattan/x.fitness for x in self.population])
        probabilities = []
        for chromosome in self.population:
            probabilities.append((manhattan/chromosome.fitness) / totalFitness)
        return numpy.random.choice(self.population, self.parentSize, probabilities).tolist()

    def uniform_crossover(self, parent1, parent2):
        """
        Performs Uniform Crossover of two parents.
        :param: 2 parent chromosomes to crossover.
        :returns: 2 new child chromosomes.
        """
        path1 = []
        path2 = []
        for index in range(self.chromosomeSize):
            if random() < 0.5:
                path1.append(parent1.path[index])
                path2.append(parent2.path[index])
            else:
                path2.append(parent1.path[index])
                path1.append(parent2.path[index])
        return [Chromosome(self.world, path=path1), Chromosome(self.world, path=path2)]

    def selection(self):
        """
        Performs selection in the population.
        :returns: None
        """
        newPopulation = self.population[:self.populationSize]
        self.population = newPopulation

    def find_best_chromosome(self):
        """
        Updates the fittest chromosome in the population.
        Checks if the fitness value of the last chromosome changes and updates the generations counter.
        :returns: None
        """
        newBestChrom = self.population[0]
        if self.bestChromosome and newBestChrom.fitness == self.bestChromosome.fitness:
            self.sameFittestGenerations += 1
        else:
            self.sameFittestGenerations = 0
        self.bestChromosome = newBestChrom

    def print_status(self):
        """
        Prints the current generation and the fittest chromosome.
        :returns: None
        """
        string = "Generation: {}".format(self.generation)
        string += "\tBest path found: {}".format(self.bestChromosome)
        print(string)

    def update_data(self):
        """
        Updates the data of the generation:
            1. Max fitness value.
            2. Min fitness value.
            3. Average fitness value.
        :returns: None
        """
        values = [x.fitness for x in self.population]
        self.data[self.generation] = {"max": max(values),
                                      "min": min(values),
                                      "avg": sum(values)/len(values)}

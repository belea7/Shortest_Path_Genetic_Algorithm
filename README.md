Genetic algorithm that finds the shortest path between two points on a grid (with obstacles).
---------------------------------------------------------------------------------------------
The program implements the genetic algorithm entirely (without using external modules).
Python modules: tkinter, matplotlib, arg, numpy.
"Biological Computation" course at The Open University of Israel.

I used genetic algorithm to find the shorttest path between two points in a grid (whose size is not constant).
The program receives as an argument the size of the grid which consists the world, creates random start and finish points and uses genetic algorithm to find the shorttest path.
The program automatically decides the paramaters of the genetic algorithm (populaion size, mutation and mutation probability, size of the elite group and the parents group (in percentages).
The algorithm also receives number of obstacles that can be placed on the grid, and places them randomly on the grid.The algorithm builds a path that avoids bumping into obstacles.

While running the program prints helful messages that help track its progress in every generation and finally prints the path chosen by the algorithm.

When the algorithm finishes running it prints the view of the world, including the starting and points, the path chosen and the obstacles (using tkinter module).

After exiting the tkinter window, the program displays statistics.

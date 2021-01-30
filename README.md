Genetic algorithm that finds the shortest path between two points on a grid (with obstacles)
---------------------------------------------------------------------------------------------
The program implements the genetic algorithm entirely (without using external modules).

Python modules: tkinter, matplotlib, arg, numpy.

**Biological Computation** course at The Open University of Israel.

I used genetic algorithm to find the shorttest path between two points in a grid (whose size is not constant).
The program receives as an argument the size of the grid which consists the world, creates random start and finish points and uses genetic algorithm to find the shorttest path.
The program automatically decides the paramaters of the genetic algorithm (populaion size, mutation and mutation probability, size of the elite group and the parents group (in percentages).
The algorithm also receives number of obstacles that can be placed on the grid, and places them randomly on the grid.The algorithm builds a path that avoids bumping into obstacles.

While running the program prints helful messages that help track its progress in every generation.
```
Generation: 110 
Best path found: Path: Down , Right , Right , Down , Right , Right , Down , Down , Down , Right , Down , Down , Down , Right , Down , Down , Down , Down , Down , Down , Down , Right , Down , Right , Right , Down , Right , Down , Down , Up , Right , Down , Down , Down , Up , Down , Up , Right , Down , Left , Right , Down , Left , Left , Right , Right , Down , Right , Down , Down , Down , Down , Down , Right , Right , Down , Down , Down , Right , Left , Down , Right , Up , Down , Down , Right , Left , Up , Down , Down , Down , Down , Left , Right , Up , Down , Down , Right , Down , Left , Down , Left , Right , Up , Right , Right , Left , Right , Right , Up , Down , Down , Up , Up , Left , Down , Down , Right , Right , Up 
Fitness: 29
PATH FOUND.
```

When the algorithm stops it prints the path chosen by the algorithm.
```
Found best path from (20, 39) to (1, 49)
(Manhattan Distance: 29)
29 moves: Down , Right , Right , Down , Right , Right , Down , Down , Down , Right , Down , Down , Down , Right , Down , Down , Down , Down , Down , Down , Down , Right , Down , Right , Right , Down , Right , Down , Down
```

When the algorithm finishes running it prints the view of the world, including the starting and points, the path chosen and the obstacles (using tkinter module).

After exiting the tkinter window, the program displays statistics.

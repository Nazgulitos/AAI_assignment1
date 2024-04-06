# Avengers and Infinity Stone Pathfinding using A* and backtracking algorithms

## Overview

This repository contains two different algorithms implemented in Python for finding the shortest path from a starting position to the Infinity Stone while navigating through a map filled with obstacles (Avengers). The algorithms employed are A* algorithm and backtracking algorithm.

## A* Algorithm

The A* algorithm, implemented in `astar_algorithm.py`, is utilized to find the shortest path from a starting node to the Infinity Stone on a 9x9 map. Here's a brief summary of its functionality:

- Utilizes the A* algorithm leveraging the heap queue algorithm for efficiency.
- Interacts with the environment by detecting the presence of Avengers and updating the map accordingly.
- Maintains an open set of nodes to be evaluated and a closed set of nodes that have already been evaluated.
- Iteratively selects the node with the lowest combined cost (actual cost + heuristic) from the open set and explores its neighbors.
- Updates the costs if a more efficient path is found.
- Continues this process until the goal node (Thanos finding the Infinity Stone) is reached or the open set is empty.
- Provides the shortest path from the starting position to the Infinity Stone.

## Backtracking Algorithm

The backtracking algorithm, implemented in `backtracking_algorithm.py`, explores the map in search of the shortest path from the starting position to the coordinates of the Infinity Stone. Here's a brief summary of its functionality:

- Performs exploration in a depth-first manner, making moves to adjacent positions and backtracking when necessary.
- Uses a recursive function `explore_map` to simulate Thanos' movements on the map while considering constraints and avoiding encounters with Avengers.
- Maintains a matrix to track visited positions and utilizes memoization to optimize the search for the shortest path in the second phase.
- Initializes parameters for the backtracking algorithm with the `explore_map_2` method and implements backtracking logic with memoization in the `find_path` method.
- Terminates when it finds the shortest path or explores the entire map without finding a valid path.

## Limitations

1. The A* algorithm allows teleportation, causing it to fail the second half of tests on codeforces.
2. Neither A* nor the backtracking algorithm accounts for the presence of a shield.
3. Neither A* nor the backtracking algorithm manage choosing a variant of the perception zone. This choice doesn't affect gameplay.
4. In the backtracking algorithm, the program first fully explores the map, communicating with the interactor, before finding the shortest path.

## License

This project is licensed under the [MIT License](LICENSE).

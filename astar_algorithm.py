"""Module Description: This module implements the heap queue algorithm
 (priority queue algorithm)."""
import heapq
import sys

# The initial 9x9 map without constraints
board = [[0] * 9 for _ in range(9)]

avengers = ["H", "T", "M", "P"]
# 1 or 2 - variants of Thanos perception zones
variant = int(input())
# Start and goal positions
start = (0, 0)
input_str = input()
goal = tuple(map(int, input_str.split()))


def heuristic(current_coordinates, previous_coordinates):
    """
    Function counts difference between current and previous coordinates
    :param current_coordinates:  x-axis coordinate
    :param previous_coordinates: y-axis coordinate
    :return: difference between current and previous coordinates
    """
    return abs(current_coordinates[0] - previous_coordinates[0])\
        + abs(current_coordinates[1] - previous_coordinates[1])


def print_current_map(x_coordinate, y_coordinate):
    """
    Function prints the current state of a map with items(P, H, T, M, I)
    :param x_coordinate: x-axis coordinate
    :param y_coordinate: y-axis coordinate
    :return: none
    """
    for i in range(9):
        for j in range(9):
            if j == x_coordinate and i == y_coordinate:
                print("A", end=' ')
            elif board[j][i] == 1:
                print(".", end=' ')
            else:
                print(board[j][i], end=' ')
        print()


def get_map_response():
    """
    Function implements Reading input from interactor
    :return: none
    """
    response = int(input())  # number of current items around Thanos
    if response > 0:
        for _ in range(response):
            info = input().split()
            item_x, item_y, item_type = map(str, info)
            if item_type in avengers:
                board[int(item_x)][int(item_y)] = 1
            else:
                board[int(item_x)][int(item_y)] = 0
            # Case, when the Thanos coincides with Avenger
            # and have no chance to survive
            if int(item_x) == 0 and int(item_y) == 0:
                print("e -1")
                sys.exit(0)


def astar(game_board, start_coordinates, goal_coordinates):
    """
    Function implements A-star algorithm.
    :param game_board: initial map with constraints
    :param start_coordinates: a couple of Thanos start coordinates
    :param goal_coordinates: a couple of Infinity Stone coordinates
    :return: None, if path wasn't found, else - nothing
    """
    open_set = []
    heapq.heappush(open_set, (0, start_coordinates))
    came_from = {}

    # Represents the cost of the path from the start node to the current node
    g_score = {start_coordinates: 0}

    # Represents the estimated total cost from the start node to the goal node
    # passing through the current node
    f_score = {start_coordinates: heuristic(start_coordinates,
                                            goal_coordinates)}
    while open_set:
        # Current move is taken from priority queue
        current = heapq.heappop(open_set)[1]
        print(f"m {current[0]} {current[1]}")
        # Checking whether the program reached the Infinity Stone
        if current == goal_coordinates:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start_coordinates)
            return path[::-1], g_score[goal_coordinates]

        # Interactor calling
        get_map_response()

        # Checking all possible moves from current
        for neighbor in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (current[0] + neighbor[0], current[1] + neighbor[1])

            if (new_position[0] < 0
                    or new_position[0] >= len(game_board)
                    or new_position[1] < 0
                    or new_position[1] >= len(game_board[0])
                    or game_board[new_position[0]][new_position[1]] == 1):
                continue

            # The sum of the known cost to reach the current node
            tentative_g_score = g_score[current] + 1

            if (new_position not in g_score
                    or tentative_g_score < g_score[new_position]):
                came_from[new_position] = current
                g_score[new_position] = tentative_g_score
                f_score[new_position] = (tentative_g_score
                                         + heuristic(new_position, goal_coordinates))
                heapq.heappush(open_set, (f_score[new_position], new_position))

    # Path not found
    return None, None


# Run the A* algorithm
path, path_length = astar(board, start, goal)
if path:
    print(f"e {path_length}")
else:
    print("e -1")

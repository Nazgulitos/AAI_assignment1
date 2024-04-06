"""Module providing access to some variables and functions that
 interact strongly with the Python interpreter."""
import sys


class Map:
    """Class representing a map"""

    def __init__(self):
        self.matrix = [[1 for _ in range(9)] for _ in range(9)]
        self.visited = [[0 for _ in range(9)] for _ in range(9)]


class PathFinder:
    """Class representing parameters for finding the shortest path"""

    def __init__(self, infinity_stone_coordinates):
        """
        :param infinity_stone_coordinates: x-axis any y-axis coordinates of inf stone on the map
        """
        self.short_length = None
        self.has_path = None
        self.length = None
        self.memo = None
        self.infinity_stone_coordinates = infinity_stone_coordinates


class GameEnvironment:
    """Class representing a game"""

    def __init__(self, variant_, infinity_stone_coordinates):
        """
        Function initializes parameters of a game
        :param variant_: represents variant of Thanos perception
        :param infinity_stone_coordinates: x and y coordinates of an infinity stone on the map
        """
        self.variant = variant_
        self.map = Map()
        self.path_finder = PathFinder(infinity_stone_coordinates)
        self.moves = 0
        self.cnt = 0
        self.cnt2 = 0
        self.steps = []
        self.current_i = -1
        self.flag = 0  # 1, when the Thanos at dead end and goes back

    # def print_current_map(self, x_coordinate, y_coordinate):
    #     """
    #     Function prints the current state of a map with items(P, H, T, M, I)
    #     :param x_coordinate: x-axis coordinate
    #     :param y_coordinate: y-axis coordinate
    #     :return: none
    #     """
    #     for i in range(9):
    #         for j in range(9):
    #             if j == x_coordinate and i == y_coordinate:
    #                 print("A", end=' ')
    #             elif self.map.matrix[j][i] == 1:
    #                 print(".", end=' ')
    #             else:
    #                 print(self.map.matrix[j][i], end=' ')
    #         print()

    def explore_map(self, x_coordinate, y_coordinate):
        """
        Function uses backtracking algorithm to make moves from current state
        to explore map, perceiving items around
        state from the interactor. Exploring the map,
        it creates a map with all possible constraint items.
        :param x_coordinate: x-axis coordinate
        :param y_coordinate: y-axis coordinate
        :return: none
        """
        # The program should visit new place on the map only once.
        if self.map.visited[x_coordinate][y_coordinate] == 1 and self.flag == 1:
            return
        self.map.visited[x_coordinate][y_coordinate] = 1
        print(f"m {x_coordinate} {y_coordinate}")
        self.steps.append([x_coordinate, y_coordinate])
        self.current_i += 1

        # self.print_current_map(x_coordinate, y_coordinate)

        # If the program reached the inf stone coordinates,
        # it can call the next function to find the shortest path.
        # Counters show that the program wasn't in each place more than one time.
        if not (not (self.path_finder.infinity_stone_coordinates[0] == x_coordinate and
                     self.path_finder.infinity_stone_coordinates[1] == y_coordinate) and
                not self.cnt > 100) or self.cnt2 > 100:
            self.explore_map_2()
            sys.exit(0)

        sys.stdout.flush()
        # Reading input from interactor
        response = int(input())  # number of current items around Thanos
        if response > 0:
            for _ in range(response):
                info = input().split()
                item_x, item_y, item_type = map(str, info)
                self.map.matrix[int(item_x)][int(item_y)] = item_type
                # Case, when the Thanos coincides with Avenger and have no chance to survive
                if int(item_x) == 0 and int(item_y) == 0:
                    print("e -1")
                    sys.exit(0)

        # All possible moves of Thanos.
        moves = [(x_coordinate + 1, y_coordinate), (x_coordinate, y_coordinate + 1),
                 (x_coordinate - 1, y_coordinate), (x_coordinate, y_coordinate - 1)]

        avengers = ["H", "T", "M", "P"]

        # Making moves using backtracking method.
        for move in moves:
            new_x, new_y = move
            if 0 <= new_x < 9 and 0 <= new_y < 9 and not \
                    self.map.visited[new_x][new_y] and \
                    self.map.matrix[new_x][new_y] not in avengers:
                self.moves += 1
                self.flag = 1
                self.explore_map(new_x, new_y)
                self.cnt += 1
                self.moves -= 1

        # If Thanos at a dead end, he goes back.
        self.steps.pop(-1)
        self.current_i -= 1
        if self.current_i >= 0:
            self.flag = 0
            self.cnt2 += 1
            x_coordinate = int(self.steps[self.current_i][0])
            y_coordinate = int(self.steps[self.current_i][1])
            return self.explore_map(x_coordinate, y_coordinate)
        return None

    def explore_map_2(self):
        """
        Preparing function for implementing backtracking algorithm
        that initializes necessary objects and variables.
        :return: none
        """
        self.map.visited = [[0 for _ in range(len(self.map.matrix[0]))]
                            for _ in range(len(self.map.matrix))]
        self.path_finder.memo = [[-1 for _ in range(len(self.map.matrix[0]))]
                                 for _ in range(len(self.map.matrix))]
        start = (0, 0)
        end = (self.path_finder.infinity_stone_coordinates[0],
               self.path_finder.infinity_stone_coordinates[1])

        self.path_finder.short_length = sys.maxsize
        self.path_finder.length = 0
        self.path_finder.has_path = False

        self.find_path(start, end)
        if self.path_finder.has_path:
            print(f"e {self.path_finder.short_length}")
        else:
            print("e -1")

    def find_path(self, start, end):
        """
        Function implements backtracking algorithm using memoization for efficiency.
        :param start: current x-axis coordinate
        :param end: current y-axis coordinate
        :return: none
        """
        x_coordinate, y_coordinate = start
        end_x, end_y = end

        # The program reaches inf stone, checking whether it was the shortest path.
        if x_coordinate == end_x and y_coordinate == end_y:
            self.path_finder.has_path = True
            self.path_finder.short_length = \
                min(self.path_finder.length, self.path_finder.short_length)
            return

        if self.path_finder.memo[x_coordinate][y_coordinate] != -1 and \
                self.path_finder.memo[x_coordinate][y_coordinate] <= self.path_finder.length:
            return

        self.path_finder.memo[x_coordinate][y_coordinate] = self.path_finder.length

        if self.path_finder.length > self.path_finder.short_length:
            return

        self.map.visited[x_coordinate][y_coordinate] = 1
        self.path_finder.length += 1

        if self.can_visit(x_coordinate + 1, y_coordinate):
            self.find_path((x_coordinate + 1, y_coordinate), end)

        if self.can_visit(x_coordinate, y_coordinate + 1):
            self.find_path((x_coordinate, y_coordinate + 1), end)

        if self.can_visit(x_coordinate - 1, y_coordinate):
            self.find_path((x_coordinate - 1, y_coordinate), end)

        if self.can_visit(x_coordinate, y_coordinate - 1):
            self.find_path((x_coordinate, y_coordinate - 1), end)

        self.map.visited[x_coordinate][y_coordinate] = 0
        self.path_finder.length -= 1

    def can_visit(self, x_coordinate, y_coordinate):
        """
        Helping function for implementing backtracking algorithm
        that check whether is coordinates are visitable.
        :param x_coordinate: x-axis coordinate
        :param y_coordinate: y-axis coordinate
        :return: True(if the place is visitable), False (otherwise)
        """
        if x_coordinate < 0 or y_coordinate < 0 or x_coordinate >= len(self.map.visited[0]) \
                or y_coordinate >= len(self.map.visited):
            return False
        if self.map.matrix[x_coordinate][y_coordinate] == 0 or \
                self.map.visited[x_coordinate][y_coordinate] == 1:
            return False
        return True


variant = int(input())
infinity_stone_x, infinity_stone_y = map(int, input().split())

game = GameEnvironment(variant, (infinity_stone_x, infinity_stone_y))

game.explore_map(0, 0)

print("e -1")
sys.exit(0)

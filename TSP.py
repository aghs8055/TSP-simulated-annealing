from typing import Union, Dict, List
from random import randint, choice, uniform
import math

from matplotlib import pyplot as plt


class Point:
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        self.x = x
        self.y = y

    def __sub__(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class TSP:
    def __init__(
        self,
        points: Dict[Union[str, int], Point],
        init_temp: int = 1000,
        alpha: int = 0.99,
        same_solution: int = 150000,
    ):
        self.points = points
        self.point_count = len(self.points)
        self.init_temp = init_temp
        self.alpha = alpha
        self.target_same_solution = same_solution
        self.solution = list(self.points.keys())
        self.distances = {
            j: {i: self.points[i] - self.points[j] for i in points} for j in points
        }
        self.cost = self.calculate_distance(self.solution)

    def get_new_solution(self):
        new_solution_generator = [
            self.inverse_path,
            self.swap_point,
            self.change_point_position,
            self.change_path_position,
        ]
        return choice(new_solution_generator)()

    def inverse_path(self):
        start_index = randint(0, self.point_count - 2)
        end_index = randint(start_index + 1, self.point_count - 1)
        new_solution = self.solution.copy()
        new_solution[start_index : end_index + 1] = reversed(
            new_solution[start_index : end_index + 1]
        )
        return new_solution

    def swap_point(self) -> List[Union[int, str]]:
        first = randint(0, self.point_count - 2)
        second = randint(first + 1, self.point_count - 1)
        new_solution = self.solution.copy()
        new_solution[first], new_solution[second] = (
            new_solution[second],
            new_solution[first],
        )
        return new_solution

    def change_point_position(self) -> List[Union[int, str]]:
        first = randint(0, self.point_count - 1)
        second = randint(0, self.point_count - 1)
        new_solution = self.solution.copy()
        value = new_solution.pop(first)
        new_solution.insert(second, value)
        return new_solution

    def change_path_position(self) -> List[Union[int, str]]:
        start_index = randint(0, self.point_count - 2)
        end_index = randint(start_index + 1, self.point_count - 1)
        new_solution = self.solution.copy()
        value = new_solution[start_index : end_index + 1]
        new_solution = new_solution[:start_index] + new_solution[end_index + 1 :]
        break_index = randint(0, len(new_solution))
        new_solution = new_solution[:break_index] + value + new_solution[break_index:]
        return new_solution

    def calculate_distance(self, solution: List[Union[int, str]]) -> int:
        distance = 0
        for i in range(self.point_count - 1):
            distance += self.distances[solution[i]][solution[i + 1]]
        distance += self.distances[solution[-1]][solution[0]]
        return distance

    def solve(self):
        cur_temp = self.init_temp
        same_solution = 0
        old_solution = self.solution
        old_cost = self.cost

        while same_solution < self.target_same_solution:
            new_solution = self.get_new_solution()
            new_cost = self.calculate_distance(new_solution)
            if new_cost < self.cost:
                self.solution = new_solution
                self.cost = new_cost
            if new_cost < old_cost:
                old_cost = new_cost
                old_solution = new_solution
                same_solution = 0
            elif new_cost == old_cost:
                same_solution += 1
            else:
                if uniform(0, 1) < math.exp(
                    float(old_cost - new_cost) / float(cur_temp)
                ):
                    old_cost = new_cost
                    old_solution = new_solution
                    same_solution = 0
                else:
                    same_solution += 1
            cur_temp *= self.alpha

    def display_solution(self):
        x = [self.points[point_name].x for point_name in self.solution] + [
            self.points[self.solution[0]].x
        ]
        y = [self.points[point_name].y for point_name in self.solution] + [
            self.points[self.solution[0]].y
        ]
        plt.plot(x, y, "o-")
        plt.show()

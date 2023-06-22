import pandas
from TSP import Point, TSP


if __name__ == "__main__":
    data = pandas.read_csv("data.csv", header=None, names=["name", "x", "y"])
    data = data.set_index("name").apply(tuple, axis=1).to_dict()
    points = {
        name: Point(coordinates[0], coordinates[1])
        for name, coordinates in data.items()
    }
    tsp = TSP(points, same_solution=1500)
    tsp.solve()
    print(f'Cost of final solution: {tsp.cost}')
    tsp.display_solution()

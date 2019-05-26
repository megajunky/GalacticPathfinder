from BinaryHeap import BinaryHeap
from Graph import Graph
from functools import reduce
import json, time

def find(graph, start, goal):
    open_list = BinaryHeap()

    closed_list = {}

    open_list.insert((0, start, start))

    while not open_list.is_empty():
        dist, cur, came_from = open_list.extract_min()

        if cur in closed_list and dist > closed_list[cur][0]:
            continue 

        closed_list[cur] = (dist, came_from)

        if cur == goal:
            break

        for cost, neig in graph.neighbors(cur):
            open_list.insert((dist + cost, neig, cur))

    return closed_list


def retrace_path(closed_list, start, goal, path=[]):
    if start == goal:
        return path

    cost, prev = closed_list[goal]
    path.append((cost, prev))

    return retrace_path(closed_list, start, prev, path)


if __name__ == "__main__":
    graph = Graph()
    graph.from_json("graph.json")

    start = graph.find("Erde")
    end = graph.find("b3-r7-r4nd7")

    closed_list = find(graph, start, end)
    path = retrace_path(closed_list, start, end)
    total_dist = reduce(lambda a,c: a+c[0], path, 0)

    print("Path:" + "".join(f"{node} -> " for _, node in reversed(path)) + str(end))
    print(f"Total Distance: {total_dist}")


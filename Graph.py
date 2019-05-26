from functools import reduce
import json, time

class Graph:
    def __init__(self):
        self.edges = {}
        self.nodes = []

    def find(self, label):
        return self.nodes.index(label)
    def neighbors(self, node):
        if node in self.edges:
            return self.edges[node]

        return []
    
    def from_json(self, path):
        def reducer(acc, cur):
            s = cur['source']
            t = cur['target']
            c = cur['cost']
            if s not in acc:
                acc[s] = []
            acc[s].append((c, t))
            if t not in acc:
                acc[t] = []
            acc[t].append((c,s))
            return acc

        f = open(path)
        data = json.load(f)
        self.edges = reduce(reducer, data["edges"], {})
        self.nodes = list(map(lambda x: x["label"], data["nodes"]))


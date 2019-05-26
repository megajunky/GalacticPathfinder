from heapq import heappush, heappop
class BinaryHeap:
    def __init__(self):
        self.queue = []
        
    def insert(self, e):
        heappush(self.queue, e)

    def extract_min(self):
        return heappop(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

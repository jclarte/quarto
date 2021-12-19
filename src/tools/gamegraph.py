"""
custom class to handle graph stuff
"""

from collections import defaultdict
import networkx as nx

class GameGraph(nx.DiGraph):
    """
    acyclic graph with single ancestor with simple algorithm and data structure
    """

    def __init__(self, game:):
        super().__init__()
        

    def add_node(self, node):
        if self.root is None:
            self.root = node

    def add_edge(self, edge):
        pass

    def prune(self, node):
        pass

    


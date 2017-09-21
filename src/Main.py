from sys import argv
import GraphGen

class Main:
    def __init__(self, k, N):
        self.ID = ''
        self.graph = GraphGen.GraphGen(self.ID, k, N)

    def run(self):
        paths, graph_weights = self.graph.generateGraph()
        total_cost = self.graph.genShortestPathGraph(paths, graph_weights)
        self.graph.outputData(paths, total_cost)

if __name__ == '__main__':
    if len(argv) < 3:
        print('Usage: python Main.py <argument-1> <argument-2>')
        print('Argument-1: Number of Nodes')
        print('Argument-2: Parameter k ')
    else:
        N = argv[1]
        k = argv[2]
        main_program = Main(k,N)
        main_program.run()

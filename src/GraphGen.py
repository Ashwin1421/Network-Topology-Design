from random import sample
from matplotlib import pyplot as plt, pylab
import networkx as nx

class GraphGen:
    def __init__(self, ID, k, N):
        self.N = int(N)
        self.ID = ID
        self.k = int(k)

    def digitizeID(self, ID):
        return list(map(int,ID*3))

    def getTrafficDemandValues(self):
        D = self.digitizeID(self.ID)
        B = [[0 for x in range(len(D))] for y in range(len(D))]
        for i in range(len(D)):
            for j in range(len(D)):
                B[i][j] = abs(D[i] - D[j])

        return B

    def getEdgeCostValues(self):

        A = [[0 for x in range(self.N)] for y in range(self.N)]
        for i in range(self.N):
            j_indices = [j for j in sample(range(self.N), self.k) if j != i]
            for j in j_indices:
                A[i][j] = 1
            not_j_indices = [item for item in range(self.N) if item not in j_indices]
            for j in not_j_indices:
                A[i][j] = 300

        return A


    def generateGraph(self):

        A = self.getEdgeCostValues()
        B = self.getTrafficDemandValues()
        """
        Get edge-cost values and
        traffic demand values by given rules.
        Using these values, we set the weights for all edges.
        """
        weights = [[0 for x in range(self.N)] for y in range(self.N)]
        for i in range(self.N):
            for j in range(self.N):
                if i!=j:
                    weights[i][j] = A[i][j] * B[i][j]

        """
        Adjusting weights of edges in the graph.
        If any edge has weight as 0, we adjust it to 1.
        As there can be multiple zero weight edges in the graph.
        """
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    if weights[i][j] == 0:
                        weights[i][j] = 1


        graph_data = []

        for i in range(self.N):
            for j in range(self.N):
                if j != i:
                    graph_data.append(list(zip([i], [j], [weights[i][j]])))


        graph_data_ebunch = [item for sublist in graph_data for item in sublist]

        graph = nx.DiGraph()
        graph.add_weighted_edges_from(graph_data_ebunch, weight='weight')
        shortest_paths = nx.all_pairs_dijkstra_path(graph, weight='weight')

        return shortest_paths, weights


    def outputData(self, path_list, total_cost):
        paths_output = 'graph_data.out'
        fo = open(paths_output,'w')
        fo.write('Total Cost of Graph with N='+str(self.N)+' and k='+str(self.k)+' is '+str(total_cost)+'\n')
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    fo.write('Path from node: '+str(i)+' to node: '+str(j)+str(path_list[i][j])+'\n')
        fo.close()

    def save_graph(self, graph, file_name):
        # initialze Figure
        plt.figure(figsize=(20,20), dpi=200)
        plt.axis('off')
        fig = plt.figure(1)
        pos = nx.spring_layout(graph)
        nx.draw_networkx_nodes(graph, pos, label='Nodes')
        nx.draw_networkx_edges(graph, pos, label='Edges')
        nx.draw_networkx_labels(graph, pos)

        edge_labels = nx.get_edge_attributes(graph, 'weight')
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

        cut = 1.00
        xmax = cut * max(xx for xx, yy in pos.values())
        ymax = cut * max(yy for xx, yy in pos.values())
        plt.xlim(0, xmax)
        plt.ylim(0, ymax)
        plt.legend(numpoints = 1)
        plt.savefig(file_name, bbox_inches="tight")
        pylab.close()
        del fig


    def genShortestPathGraph(self, shortest_paths, graph_weights):

        #print(len(shortest_paths))
        new_edge_paths = []
        for i in range(self.N):
            for j in range(self.N):
                if i!= j:
                    new_edge_paths.append(shortest_paths[i][j])

        new_graph_ebunch = []
        for edge in new_edge_paths:
            for i in range(0,len(edge)-1):
                new_graph_ebunch.append((edge[i],edge[i+1],graph_weights[edge[i]][edge[i+1]]))


        new_graph = nx.DiGraph()
        new_graph.add_weighted_edges_from(new_graph_ebunch)


        edge_list = [(u,v) for (u,v,w) in new_graph.edges(data=True)]
        weight_list = [w['weight'] for (u,v,w) in new_graph.edges(data=True)]
        total_cost = sum(weight_list)
        self.save_graph(new_graph,'Shortest_Path_Graph'+'_k='+str(self.k)+'.png')

        return total_cost



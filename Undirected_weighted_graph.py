import operator


class Graph():

    def __init__(self, vertices_num):
        # number of nodes (an integer)
        self.v = vertices_num
        # (maybe not useful here) : list of nodes from "A0", "A1" ... to "A index (vertices_num - 1)"
        self.nodes = ['A' + str(x-1) for x in range(self.v)]
        self.paths = []

    # from adjacency matrix to dictionary
    def adjmat_2_graph(self, adjm:list):
        graph = {}
        if type(adjm) != list or adjm is None:
            return None
        for i in range(len(adjm)):
            char = 'A' + str(i)
            ls = []
            for j in range(len(adjm[i])):
                if adjm[i][j] > 0:
                    tp = ('A' + str(j), adjm[i][j])
                    ls.append(tp)
            graph[char] = ls
        return graph

    # from dictionary to adjacency matrix
    def graph_2_mat(self, graph):
        print(graph)
        adjm = []
        keys = list(graph.keys())
        n = len(keys)  # the amount of nodes in G
        for i in range(n):
            ls = [0 for x in range(n)]
            adjm.append(ls)
        for i in range(len(keys)):
            index = int(keys[i][1])
            tup_list = graph[keys[i]]
            for j in range(len(tup_list)):
                sec_index = int(tup_list[j][0][1:])
                weight = tup_list[j][1]
                if weight > 0:
                    adjm[index][sec_index] = weight
                    adjm[sec_index][index] = weight
        return adjm

    # from dictionary to adjacency list
    def graph_2_list(self, graph):
        lst = []
        if type(graph) != dict or graph is None:
            return None
        keys = list(graph.keys())
        for i in range(len(keys)):
            item = [keys[i], graph[keys[i]]]
            lst.append(item)
        lst = sorted(lst, key=operator.itemgetter(0))
        return lst

    # from adjacency list to dictionary
    def list_2_graph(self, lst):
        graph = {}
        for i in range(len(lst)):
            graph[lst[i][0]] = lst[i][1]
        return graph

    # from adjacency matrix to adjacency list
    def mat_2_list(self, mat):
        graph = self.adjmat_2_graph(mat)
        ls = self.graph_2_list(graph)
        return ls

    # from adjacency list to adjacency matrix
    def list_2_mat(self, lst):
        graph = self.list_2_graph(lst)
        mat = self.graph_2_mat(graph)
        return mat

    def bfs(self, graph, start_vertex):
        # graph is a dictionary
        V = list(graph.keys())
        V.remove(start_vertex)
        layers = [[start_vertex]]
        i = 0
        # layers is the list of all layers based on BFS algorithm
        while len(V) > 0:
            new_layer = []
            for vertex in layers[i]:
                for item in graph[vertex]:
                    if item[0] in V:  # means we should add that vertex to the new layer
                        new_layer.append(item[0])
                        V.remove(item[0])
            layers.append(new_layer)
            i += 1
        return layers

    # returns the layer number in which the vertex is found or -1 otherwise
    def is_in_layer(self, layers: list, vertex):
        for i in range(len(layers)):
            if vertex in layers[i]:
                return i
        return -1

    def opt(self, graph:dict, start_v:str, end_v:str, vertex:str, path_list: str):
        if vertex in path_list:
            return None
        if end_v == vertex:
            path_list += '-' + vertex
            if path_list not in self.paths:
                self.paths.append(path_list)
            return None
        if start_v == vertex and path_list == '':
            path_list = vertex
        else:
            path_list += '-' + vertex
        # now we should call all of vertex neighbors with opr
        neighbors = [x[0] for x in graph[vertex]]
        for nei in neighbors:
            self.opt(graph, start_v, end_v, nei, path_list)

    # find all path from node start_vertex to node end_vertex
    def find_all_paths(self, graph:dict, start_vertex:str, end_vertex:str):
        # graph is a dictionary
        print(graph)
        print(f'first is: {start_vertex} and last is: {end_vertex}')

        first_bfs = self.bfs(graph, start_vertex)
        if self.is_in_layer(first_bfs, end_vertex) == -1:
            print("first")
            return None
        V = list(graph.keys())
        if end_vertex not in V or start_vertex not in V:
            print("second")
            return None
        if start_vertex == end_vertex:
            return [start_vertex]

        self.opt(graph, start_vertex, end_vertex, start_vertex, '')
        i = 0
        while i < len(self.paths):
            if self.paths[i][-2:] != end_vertex or self.paths[i][:2] != start_vertex:
                del self.paths[i]
                i -= 1
            i += 1

        return sorted(sorted(self.paths, key=str), key=len)

def main():
    G = Graph(6)
    graph = {'A5': [('A3', 1)], 'A3': [('A0', 1), ('A2', 1)], 'A0': [('A3', 1), ('A5', 1)], 'A4': [('A2', 1)], 'A1': [('A2', 1)], 'A2': [('A1', 1), ('A2', 1), ('A3', 1), ('A4', 1)]}
    print(G.find_all_paths(graph,'A0','A2'))


if __name__ == '__main__':
    main()
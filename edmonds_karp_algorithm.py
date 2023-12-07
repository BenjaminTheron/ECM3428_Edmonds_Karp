"""Executes the Edmonds Karp algorithm on a provided graph"""
import math
import time


class Graph():
    """
    A class representing a network of nodes and the directed edges connecting
    them.

    Attributes:
        num_nodes (int): The number of nodes in the graph, provided as an int
            so each node can have all their edges stored in a corresponding
            index in an array.
        source (int): The node from which all algorithms and operations on
            the graph must start, stored as an integer so that it directly
            corresponds to an index in the array storing the edges for each
            node.
        sink (int): The node from which all algorithms in the graph end,
            stored as an integer so that it directly corresponds to an index
            in the array storing the edges for each node.
    """

    def __init__(self, num_nodes: int, source: int, sink: int) -> None:
        """
        A constructor method which initialises each of the Graph class
        attributes.

        Args:
            num_nodes (int): The number of nodes in the graph. Justification
                can be seen above.
            source (int): The integer representing the node to start any
                algorithms from. Justification can be seen above.
            sink (int): The integer representing the node to end any
                algorithms at. Justification can be seen above.
        """
        self.num_nodes = num_nodes
        # As the source and sink correspond to the indices in an array which
        # starts from index 0, one must be subtracted so that they correspond
        # to the correct nodes.
        self.source = source - 1
        self.sink = sink - 1

        # The adjacency matrix for the graph is initialised as an array with
        # num_nodes different empty arrays which will store each of the edges
        # associated with the node at a given index.
        self.graph = [0] * self.num_nodes
        for i in range(0, num_nodes):
            self.graph[i] = []

    def add_edge(self, from_node: int, to_node: int, capacity: int) -> None:
        """
        Creates a directed edge between a specified start and end node. This
        is done by creating an Edge object for the intended edge and the
        residual edge, with all the specified arguments.

        Args:
            from_node (int): The node that the edge starts from, provided as
                an int for the aforementioned reason.
            to_node (int): The node that edge points (is directed) to,
                provided as an int for the aforementioned reason.
            capacity (int): The amount of flow that can pass through a given
                edge, provided as an integer for ease of manipulation.
        """
        # Creates a edge object with a specified capacity, start and end point
        directed_edge = Edge(capacity, from_node, to_node)
        # Creates an edge object to represent the residual edge of the above
        residual_edge = Edge(0, to_node, from_node)

        # Sets the residual of each edge to the other edge's corresponding
        # residual
        directed_edge.residual = residual_edge
        residual_edge.residual = directed_edge

        # Adds both edges to the adjacency matrix representing the graph
        self.graph[from_node-1].append(directed_edge)
        self.graph[to_node-1].append(residual_edge)

    def bfs(self) -> int:
        """
        For the current graph object an unweighted breadth first search is
        carried out, finding the bottleneck value (largest value) that can be
        passed through the current augmentation path through the graph.

        Returns:
            network_flow (int): The smallest amount of flow that can be passed
            through the augmentation path found via the breadth first search.
            Stored as an integer for ease of manipulation.
        """
        # Queue to store the neighbours of the nodes that have been visited
        bfs_queue = []
        # Queue to store which nodes have been visited
        # Initialised so that all nodes start as unvisited
        visited = [False] * self.num_nodes
        # Visit the starting node and add it to the bfs queue
        visited[self.source] = True
        bfs_queue.append(self.source)
        # Stores the edge taken to get to each vertex (initialised to none)
        previous = [None] * self.num_nodes

        # Keep looping while there are elements in the bfs queue to visit
        while len(bfs_queue) != 0:
            # The current node is the node at the front of the bfs queue
            current_vertex = bfs_queue.pop(0)

            # Once the sink has been reached, end the loop
            if current_vertex == self.sink:
                break

            # Add every neighbouring node to the queue of nodes to visit
            for edge in self.graph[current_vertex]:
                # If the edge from the current node is not saturated and has
                # not been visited...
                if edge.remaining_capacity() > 0 and (visited[edge.to_node]
                                                      is not True):
                    # The edge is added to the visited array and the edge is
                    # stored as the previous edge for the node the edge
                    # connects to
                    visited[edge.to_node] = True
                    previous[edge.to_node] = edge
                    # The neighbouring node is added to the queue so that it
                    # will be visited later
                    bfs_queue.append(edge.to_node)

        # Returns a flow of 0 if the sink node has not been reached after
        # running the bfs search.
        if previous[self.sink] is None:
            return 0

        # Stores the smallest value that can be passed through the current
        # augmentation path through the network
        network_flow = math.inf
        edge = previous[self.sink]
        # Starting from the sink, this loop back tracks through each edge
        # until the source is reached
        while edge is not None:
            # Updates the current flow value through the network and backtracks
            network_flow = min(network_flow, edge.remaining_capacity())
            edge = previous[edge.from_node]

        edge = previous[self.sink]
        # Starting from the sink, the capacity values at each edge in the
        # augmentation path are updated
        while edge is not None:
            # Adds the bottleneck value to each node in the augmentation path
            edge.flow += network_flow
            # Subtracts the current flow through the network from each
            # residual edge in the augmentation path
            edge.residual.flow -= network_flow
            # Backtracks
            edge = previous[edge.from_node]

        return network_flow

    def edmonds_karp(self) -> int:
        """
        Executes the Edmonds-Karp algorithm on the current Graph object,
        carrying out an unweighted breadth first search on the provided flow
        graph until no more flow can be passed through the graph (no more
        augmentation paths can be found).

        Returns:
            max_flow (int): The maximum flow (largest value) that can be
                passed through a provided flow network. Used as an integer
                for ease of manipulation.
        """
        max_flow = 0
        flow = 1
        # Searches the flow graph via a bfs search while augmentation paths
        # are being found
        while flow > 0:
            # Calculates the bottleneck for an augmentation path
            flow = self.bfs()
            # Updates the graph's max flow value
            max_flow += flow

        return max_flow

    def to_string(self) -> None:
        """
        Outputs the values of each attribute and each edge object within, a
        Graph object.
        """
        print(f"Number of nodes: {self.num_nodes},",
              f"source node: {self.source},",
              f"sink node: {self.sink}")

        # Outputs the formatted output for each Edge object within the graph
        for node in self.graph:
            for edge in node:
                print(edge.to_string())


class Edge():
    """A class representing an individual edge within a flow network"""

    def __init__(self, capacity: int, from_node: int, to_node: int) -> None:
        """
        A constructor method which initialises each of the attributes for an
        Edge object.

        Args:
            capacity (int): The amount of flow that can be passed through this
                edge. This is an integer for ease of manipulation.
            from_node (int): The integer representing the node this edge comes
                from. This is an integer for ease of manipulation.
            to_node (int): The integer representing the node this edge is
                directed at. This is an integer for ease of manipulation.
        """
        self.capacity = capacity
        # These values must be decremented by one for the same reason as the
        # source and sink nodes in a Graph object
        self.from_node = from_node - 1
        self.to_node = to_node - 1
        # Before the algorithm commences every edge has a flow of 0
        self.flow = 0
        # Set to 0 as a placeholder. This represents the residual (edge moving
        # in the opposite direction with opposite flow) of this edge
        self.residual = 0

    def remaining_capacity(self) -> int:
        """
        Calculates and returns the remaining capacity for the current Edge
        object.

        Returns:
            self.capacity-self.flow (int): An integer representing the amount
                of flow that can still be passed through the current Edge
                object.
        """
        return self.capacity - self.flow

    def to_string(self) -> None:
        """Formats and outputs every attribute of the current Edge object"""
        print(f"from: {self.from_node},",
              f"to: {self.to_node},",
              f"Capacity: {self.capacity},",
              f"flow: {self.flow},",
              f"residual: {self.residual}")


if __name__ == "__main__":
    # Creates a graph with 10 nodes, where the source is node 1 and the sink
    # node 10
    graph = Graph(10, 1, 10)

    # Creates 13 edges, specifying their start, end and capacity
    # Edges exiting the source
    graph.add_edge(1, 2, 5)
    graph.add_edge(1, 3, 10)

    # Internal edges
    graph.add_edge(2, 4, 5)
    graph.add_edge(2, 5, 20)
    graph.add_edge(3, 5, 5)
    graph.add_edge(3, 6, 20)
    graph.add_edge(4, 7, 10)
    graph.add_edge(4, 8, 5)
    graph.add_edge(5, 7, 100)
    graph.add_edge(6, 9, 2)
    graph.add_edge(8, 7, 100)

    # Edges entering the sink
    graph.add_edge(7, 10, 5)
    graph.add_edge(9, 10, 10)

    # Creates a graph with 11 nodes, where node 1 is the source and node 11 is
    # the sink
    graph2 = Graph(11, 1, 11)

    # Creates 18 edges, specifying their start, end and capacity
    # Edges exiting the source
    graph2.add_edge(1, 2, 5)
    graph2.add_edge(1, 3, 10)
    graph2.add_edge(1, 4, 5)

    # Internal edges
    graph2.add_edge(3, 2, 15)
    graph2.add_edge(3, 6, 20)
    graph2.add_edge(2, 5, 10)
    graph2.add_edge(6, 4, 5)
    graph2.add_edge(4, 7, 10)
    graph2.add_edge(5, 6, 25)
    graph2.add_edge(5, 8, 10)
    graph2.add_edge(6, 9, 30)
    graph2.add_edge(7, 9, 5)
    graph2.add_edge(7, 10, 10)
    graph2.add_edge(9, 5, 15)
    graph2.add_edge(9, 10, 5)

    # Edges entering the sink
    graph2.add_edge(8, 11, 5)
    graph2.add_edge(9, 11, 15)
    graph2.add_edge(10, 11, 10)

    # Validate the graphs are correctly created by viewing the to_string() of
    # each graph
    # graph.to_string()
    # graph2.to_string()

    time_start1 = time.time()
    edmonds_karp1 = graph.edmonds_karp()
    time_end1 = time.time()

    time_start2 = time.time()
    edmonds_karp2 = graph2.edmonds_karp()
    time_end2 = time.time()

    print("The max flow through the first graph is:", edmonds_karp1)
    print("The time taken to find the max flow of the first graph is:",
          time_end1 - time_start1, "\n")

    print("The max flow through the second graph is:", edmonds_karp2)
    print("The time taken to find the max flow through the second graph is:",
          time_end2 - time_start2)

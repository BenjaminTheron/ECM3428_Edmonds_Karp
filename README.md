# ECM3428_Edmonds_Karp

## Introduction
This intention of this project is to implement the Edmonds Karp algorithm clearly and efficiently, showing how
it can be applied to find the maximum flow through a flow network.

## Prerequisites and Installation
Only built in modules and libraries were used in this project, so there are no prerequisites or installations
required to use the system.

## Project Tutorial
No sophistocated file structures were used, so after installing the project simply navigate to the main folder
(cd to ../710017661_ 182345_BCT) and do the following to run the program:

  - Enter the command 'python3 edmonds_karp_algorithm.py' into a terminal and press enter.

After execution, the program will output the max flow through two pre-made graphs, as well as the time taken
by the algorithm to each find max flow value respectively. The graphical representation for the first graph can be
seen in Figure 1 of the included report.

To calculate the max flow for new graphs do the following:

  - Initialise a flow network: var_name = Graph(num_nodes, source_node_index, sink_node_index)
  - Add edges: var_name.add_edge(from_node_index, to_node_index, capacity), where from_node_index and to_node_index
    are the indicies representing the nodes the edge comes from and points to respectively.
  - Execute the Edmonds-Karp algorithm: var_name.edmonds_karp() will return the maximum flow.

Additionally, the report for the project and presentation video are included in the same directory.

## Testing
No testing was required in the spec, and so no testing was implemented.

### Notes
All functionality that was required by the specification was provided; however, there are a number of ways
in which the algorithms can be extended:

  - Add metrics to track the amount of memory consumed by the algorithm to track its space complexity.
  - Further optimise the algorithm and their operations to further reduce execution time.
  - Testing for the algorithm.

## Details

#### Authors
Benjamin Theron

#### License
MIT License

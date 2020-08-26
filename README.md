# Traveller Salesman Problem Mayhem

Basic scaffolding to test different solutions for the TSP

## How to work with this?

- Fork repository and start playing with your solution. Classical, quantum, genetic... anything you think can beat the game (but that can be executed in a local machine, with a simulator or normal CPUs).
- Add your module and class inside the "solvers" folder. Add the class name to the "active_solvers" list. You can play with this array so you don't have to execute everything everytime.
- The only requirement is to have a calculate() method that receives G(networkx), cost_matrix and starting_node. And returns a list with the optimal route

## TODO

- Improve the graph rendering to match the node position and weights
- Randomize G edge generation
- Add a test class to each calculate method

# CS 170 Project Spring 2020

Take a look at the project spec before you get started!

Requirements:

You'll only need to install networkx to work with the starter code. For installation instructions, follow: https://networkx.github.io/documentation/stable/install.html

Files:
- `parse.py`: functions to read/write inputs and outputs
- `solver.py`: where you should be writing your code to solve inputs
- `utils.py`: contains functions to compute cost and validate NetworkX graphs

When writing inputs/outputs:
- Make sure you use the functions `write_input_file` and `write_output_file` provided
- Run the functions `read_input_file` and `read_output_file` to validate your files before submitting!
  - These are the functions run by the autograder to validate submissions
  
Instruction on how to run the solver:
- Run command: `python3 solver.py inputs` on terminal. 
This command reads through all inputs file in the input folder and feed it into our solver function which solve the problem.

Imports:
- networkx is import as `nx`
- import `choice` from random (for function `greedy`)
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
- import defaultdict
- import sys
- import os


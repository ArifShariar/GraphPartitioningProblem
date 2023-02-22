# Graph Partitioning Problem
The graph partition problem is a problem in computer science in which we are given a graph and a positive number *k*, and the goal is to partition the vertices of the graph in to *k* disjoint sets such that the sum of the weights of the cut edges are minimized.

### Solution Approaches
There are many solution approaches to Graph Paritioning Problem. In this repository, we include the solution approach of Kernighan-Lin Algorithm (KL) and Fiduccia-Mattheyeses Algorithm (FM).
KL algorithm is implemented in Python and FM algorithm is implemented in CPP. 

### How To Run Codes
**Python Codes**
1. Clone the repository to you local machine.
2. Create a virtual environment.
3. Install required libraries by `pip install -r requirements.txt`
4. Run the required algorithms from their specific folders.

**CPP Codes**

1. In the terminal, navigate to project directory and create a new directory called 'build'.
 

        mkdir build 
        cd build
2. From the 'build' directory, run the following command to generate the build files: `cmake ..`
This will generate the build files according to the cmake file provided.
3. To build the project, run the following command: `cmake --build`
This will build the executable for the project.
4. To run the program, use the following command: `./FM` 
5. Give the file path as input when the prompt is shown.


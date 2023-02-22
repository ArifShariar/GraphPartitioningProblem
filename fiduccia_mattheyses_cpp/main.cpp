// GraphPartitioningGit.cpp : Defines the entry point for the console application.
//

#include <iostream>
#include "Graph.h"
#include "Vertex.h"
#include <fstream>
#include <sstream>
#include <ctime>
#include <algorithm>
#include <memory>
#include <chrono>

using namespace std;


template <typename T> bool PComp(const T  & a, const T  & b)
{
    return stoi(a->name) < stoi(b->name);
}

int totalSteps;
int totalSegments;

void createGraph(Graph& g, string filename) {

    string line;
    ifstream myfile(filename);
    if (myfile.is_open())
    {
        getline(myfile, line);
        getline(myfile, line); //Skip the first two lines
        while (getline(myfile, line))
        {
            istringstream iss(line);
            string v1, v2;
            iss >> v1 >> v1 >> v2;
            g.addEdge(v1, v2);
//            cout << "Substring: " << v1 << "  " << v2 << endl;
        }
        myfile.close();
    }
    else cout << "Unable to open file";
}

long getCost(Graph g, vector<bool> bitvector) {
    long cost = 0;
    for (int i = 0; i < bitvector.size(); i++) {
        if (bitvector[i] == 0) { //only look at vertices in left partition to avoid checking edges twice
            for (int j = 0; j < g.vertices.size(); j++) {
                if (g.isNeighbour(g.vertices[i], g.vertices[j]) && bitvector[j] == 1)
                    cost++;
            }

        }
    }
    return cost;
}

void updateGain(Graph& g, vector<bool>& bitvector, vector<bool>& locked) {

    //unique_ptr<Vertex> maxVertex(new Vertex);
    VertexPtr maxVertex = nullptr; //Maximum gain vertex initialization
    vector<VertexPtr> currentBucket;
    vector<VertexPtr> complementBucket;
    bool currentSide = g.side;
    if (!g.side) { // Tells which side's max vertex to choose
        currentBucket = g.leftBuckets;
        complementBucket = g.rightBuckets;
        bool ifFound = false;
        int index = 0;
        while (!ifFound) {
            VertexPtr bucketIndex = currentBucket.at(g.maxLeftGainIndex - index);
            while (bucketIndex) {
                // If vertex not locked
                if (!bucketIndex->name.empty() && !locked.at(stoi(bucketIndex->name) - 1)) {
                    maxVertex = bucketIndex;
                    ifFound = true;
                    break;
                }
                bucketIndex = bucketIndex->next;
            }
            index++;
            if (index >= g.maxDegree)
                break;
        }
    }
    else {
        currentBucket = g.rightBuckets;
        complementBucket = g.leftBuckets; bool ifFound = false;
        int index = 0;
        while (!ifFound) {
            VertexPtr bucketIndex = currentBucket.at(g.maxRightGainIndex - index);
            while (bucketIndex) {
                // If vertex not locked
                if (!bucketIndex->name.empty() && !locked.at(stoi(bucketIndex->name) - 1)) {
                    maxVertex = bucketIndex;
                    ifFound = true;
                    break;
                }
                bucketIndex = bucketIndex->next;
            }
            index++;
            if (index >= g.maxDegree)
                break;
        }
    }

    //Complement the block of the vertex
    int vertexName;
    if (maxVertex == nullptr) {
        //if (maxVertex->name.empty()) {
        //Maitaining balance by flipping sides
        g.side = !g.side;
        return;
    }

    vertexName = stoi(maxVertex->name);
    bitvector.at(vertexName - 1) = !bitvector.at(vertexName - 1); // vertexName-1 is the index in the vector as vertices are stored
    // in ascending order of consecutive integers.
    //Maintaining balance by flipping sides
    g.side = !g.side;
    // Lock Vertex
    locked.at(vertexName - 1) = true;
    //For each vertex neighbouring base vertex loop
    int i = 0;
    for (size_t i = 0; i < maxVertex->adjacencyList.size(); i++) {
        int currentVertexName = stoi(maxVertex->adjacencyList.at(i)->name);
        if (!locked.at(currentVertexName - 1)) { // Consider only free vertices
            if (bitvector.at(currentVertexName - 1) == currentSide) { // u is in current block
                g.incrementGain(currentBucket, maxVertex->adjacencyList.at(i), currentSide);
            }
            else { // u is in complementary block
                g.decrementGain(complementBucket, maxVertex->adjacencyList.at(i), currentSide);
            }
        }
    }


}


bool default_FM(vector<bool>& bitvector, Graph g, int& cost) {

    // Initialize Locked vertices.
    vector<bool> lockedVertices(g.vertices.size(), 0);
    //best cost in this segment
    int bestCost = cost;
    //bottom of the segment
    vector<bool> bottom = bitvector;
    //best bit vector in this segment
    vector<bool> bestBitVector = bottom;
    // Invokes a method to calculate max Degree and initializes bucket with 2*maxDegree+1 size
    g.initializeBuckets();
    //compute initial gain for the segment
    g.initializeGain(bitvector);

    //Set which side to begin, to maintain balance
    int numZeros = 0;
    for (bool v : bitvector) {
        if (v)
            numZeros++;
    }
    if (numZeros > 0 && bitvector.size() / numZeros < 2) {
        g.side = true;
    }
    //begin segment
    int i = 0;
    while (i < g.vertices.size()) {
        updateGain(g, bitvector, lockedVertices);
        totalSteps++;
        int tmpCost = getCost(g, bitvector);
        if (tmpCost < bestCost) {
            bestCost = tmpCost;
            bestBitVector = bitvector;
        }
        i++;
    }
    totalSegments++;
    if (bestCost < cost) { //is there improvement?
        bitvector = bestBitVector;
        cost = bestCost;
        return true;
    }
    bitvector = bestBitVector;
    return false;
}



vector<bool> run_algo(Graph& g, int walkterm) {

    // Randomize bitVector for initital random Partitioning.
    g.randomizeBitVector();

    //Initialize a vector of bottoms(bitVectors)
    vector< vector<bool> > bottomList;

    // Insert the current bottom in the list
    vector<bool> bottom = g.bitvector;
    bottomList.push_back(bottom);
    // get cost of the current bottom.
    int cost = getCost(g, bottom);
    vector<bool> tmpBitVector = g.bitvector;
    int pass = 0;

    while (pass < 10) {

        //bottomList.push_back(g.bitvector);
        switch (walkterm) {
            case 0: if (!default_FM(tmpBitVector, g, cost))
                    return tmpBitVector;
                break;
        }
        pass++;
    }
    return tmpBitVector;
}

int main()
{
    int input = 0;


    string filename;
    cout << "Enter the path of the input file: " << endl;
    cin >> filename;
    Graph grr;

    // Reads the csv and generates a graph object,
    //while storing vector of Vertices along with its adjacency List
    createGraph(grr, filename);
    sort(grr.vertices.begin(), grr.vertices.end(), PComp<VertexPtr>);
    // Initialize bitVector
    grr.initializeBitVector();

    totalSteps = 0;
    totalSegments = 0;
    auto start = std::chrono::high_resolution_clock :: now();
    vector<bool> bestPartition = run_algo(grr, input);
    auto end = std::chrono::high_resolution_clock :: now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end-start);
//    cout << "Best partioning is " << endl;
//    for (auto i : bestPartition)
//        cout << i << ' ';
    cout << "Best partioning Cost is " << getCost(grr, bestPartition) << endl;
    cout<< "Time taken : "<< duration.count() <<" micro seconds "<<endl;
    getchar();
    return 0;
}

#include "string"
#include "Vertex.h"

using namespace std;

Vertex::Vertex()
= default;

Vertex::Vertex(string name) {
    this->name = name;
}
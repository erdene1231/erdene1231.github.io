#include <bits/stdc++.h>
using namespace std;

class DisjointSets {
    vector<int> parent, size;
public:
    explicit DisjointSets(int count) : parent(count + 1), size(count + 1, 1) {
        iota(parent.begin(), parent.end(), 0);
    }
    int find(int vertex) {
        while (parent[vertex] != vertex) {
            parent[vertex] = parent[parent[vertex]];
            vertex = parent[vertex];
        }
        return vertex;
    }
    bool unite(int first, int second) {
        first = find(first);
        second = find(second);
        if (first == second) {
            return false;
        }
        if (size[first] < size[second]) {
            swap(first, second);
        }
        parent[second] = first;
        size[first] += size[second];
        return true;
    }
    int component_size(int vertex) {
        return size[find(vertex)];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    DisjointSets sets(vertex_count);
    int components = vertex_count, largest = 1;
    for (int edge = 0; edge < edge_count; ++edge) {
        int first, second;
        cin >> first >> second;
        if (sets.unite(first, second)) {
            --components;
            largest = max(largest, sets.component_size(first));
        }
        cout << components << ' ' << largest << '\n';
    }
}

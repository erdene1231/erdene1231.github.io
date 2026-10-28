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

struct Edge {
    int first, second;
    long long cost;
};

optional<long long> minimum_tree(int vertex_count, vector<Edge> edges) {
    sort(edges.begin(), edges.end(), [](const Edge& left, const Edge& right) {
        return left.cost < right.cost;
    });
    DisjointSets sets(vertex_count);
    int chosen = 0;
    long long total = 0;
    for (const Edge& edge : edges) {
        if (sets.unite(edge.first, edge.second)) {
            total += edge.cost;
            ++chosen;
        }
    }
    if (chosen != vertex_count - 1) {
        return nullopt;
    }
    return total;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    vector<Edge> edges(edge_count);
    for (Edge& edge : edges) {
        cin >> edge.first >> edge.second >> edge.cost;
    }
    auto answer = minimum_tree(vertex_count, edges);
    if (answer.has_value()) {
        cout << *answer << '\n';
    } else {
        cout << "IMPOSSIBLE\n";
    }
}

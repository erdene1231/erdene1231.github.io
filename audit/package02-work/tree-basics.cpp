#include <bits/stdc++.h>
using namespace std;

struct RootedTree {
    vector<int> parent, depth, subtree;
};

RootedTree analyze_tree(const vector<vector<int>>& graph) {
    int vertex_count = static_cast<int>(graph.size()) - 1;
    RootedTree result{vector<int>(vertex_count + 1),
                      vector<int>(vertex_count + 1),
                      vector<int>(vertex_count + 1, 1)};
    vector<int> order, pending{1};
    order.reserve(vertex_count);
    while (!pending.empty()) {
        int vertex = pending.back();
        pending.pop_back();
        order.push_back(vertex);
        for (int neighbor : graph[vertex]) {
            if (neighbor == result.parent[vertex]) {
                continue;
            }
            result.parent[neighbor] = vertex;
            result.depth[neighbor] = result.depth[vertex] + 1;
            pending.push_back(neighbor);
        }
    }
    for (int index = vertex_count - 1; index > 0; --index) {
        int vertex = order[index];
        result.subtree[result.parent[vertex]] += result.subtree[vertex];
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count;
    cin >> vertex_count;
    vector<vector<int>> graph(vertex_count + 1);
    for (int edge = 0; edge < vertex_count - 1; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }
    RootedTree result = analyze_tree(graph);
    for (const vector<int>* values : {&result.parent, &result.depth, &result.subtree}) {
        for (int vertex = 1; vertex <= vertex_count; ++vertex) {
            cout << (*values)[vertex] << (vertex == vertex_count ? '\n' : ' ');
        }
    }
}

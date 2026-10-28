#include <bits/stdc++.h>
using namespace std;

optional<vector<int>> topological_order(const vector<vector<int>>& graph) {
    int vertex_count = static_cast<int>(graph.size()) - 1;
    vector<int> incoming(vertex_count + 1);
    for (int vertex = 1; vertex <= vertex_count; ++vertex) {
        for (int next : graph[vertex]) {
            ++incoming[next];
        }
    }
    queue<int> ready;
    for (int vertex = 1; vertex <= vertex_count; ++vertex) {
        if (incoming[vertex] == 0) {
            ready.push(vertex);
        }
    }
    vector<int> order;
    while (!ready.empty()) {
        int vertex = ready.front();
        ready.pop();
        order.push_back(vertex);
        for (int next : graph[vertex]) {
            if (--incoming[next] == 0) {
                ready.push(next);
            }
        }
    }
    if (static_cast<int>(order.size()) != vertex_count) {
        return nullopt;
    }
    return order;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    vector<vector<int>> graph(vertex_count + 1);
    for (int index = 0; index < edge_count; ++index) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
    }
    auto order = topological_order(graph);
    if (!order.has_value()) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    for (int index = 0; index < vertex_count; ++index) {
        cout << (*order)[index] << (index + 1 == vertex_count ? '\n' : ' ');
    }
}

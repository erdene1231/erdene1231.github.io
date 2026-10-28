#include <iostream>
#include <queue>
#include <vector>
using namespace std;
using Graph = vector<vector<int>>;

Graph read_graph(int vertex_count, int edge_count) {
    Graph graph(vertex_count + 1);
    for (int edge = 0; edge < edge_count; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }
    return graph;
}

vector<int> component_representatives(const Graph& graph) {
    int vertex_count = static_cast<int>(graph.size()) - 1;
    vector<bool> visited(vertex_count + 1, false);
    vector<int> representatives;
    queue<int> pending;

    for (int start = 1; start <= vertex_count; ++start) {
        if (visited[start]) {
            continue;
        }
        representatives.push_back(start);
        visited[start] = true;
        pending.push(start);
        while (!pending.empty()) {
            int vertex = pending.front();
            pending.pop();
            for (int next : graph[vertex]) {
                if (!visited[next]) {
                    visited[next] = true;
                    pending.push(next);
                }
            }
        }
    }
    return representatives;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    Graph graph = read_graph(vertex_count, edge_count);
    vector<int> representatives = component_representatives(graph);

    cout << static_cast<int>(representatives.size()) - 1 << '\n';
    for (int index = 1; index < static_cast<int>(representatives.size()); ++index) {
        cout << representatives[0] << ' ' << representatives[index] << '\n';
    }
    return 0;
}

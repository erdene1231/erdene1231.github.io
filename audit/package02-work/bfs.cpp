#include <algorithm>
#include <iostream>
#include <queue>
#include <vector>
using namespace std;
using Graph = vector<vector<int>>;

vector<int> shortest_path(const Graph& graph, int source, int target) {
    vector<int> distance(graph.size(), -1);
    vector<int> parent(graph.size(), -1);
    queue<int> pending;
    distance[source] = 0;
    pending.push(source);

    while (!pending.empty()) {
        int vertex = pending.front();
        pending.pop();
        for (int next : graph[vertex]) {
            if (distance[next] == -1) {
                distance[next] = distance[vertex] + 1;
                parent[next] = vertex;
                pending.push(next);
            }
        }
    }

    if (distance[target] == -1) {
        return {};
    }
    vector<int> path;
    for (int vertex = target; vertex != -1; vertex = parent[vertex]) {
        path.push_back(vertex);
    }
    reverse(path.begin(), path.end());
    return path;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int vertex_count, edge_count, source, target;
    cin >> vertex_count >> edge_count >> source >> target;
    Graph graph(vertex_count + 1);
    for (int edge = 0; edge < edge_count; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }

    vector<int> path = shortest_path(graph, source, target);
    if (path.empty()) {
        cout << "IMPOSSIBLE\n";
    } else {
        cout << path.size() << '\n';
        for (int vertex : path) {
            cout << vertex << ' ';
        }
        cout << '\n';
    }
    return 0;
}

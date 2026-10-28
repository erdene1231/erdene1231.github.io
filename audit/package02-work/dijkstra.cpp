#include <bits/stdc++.h>
using namespace std;

constexpr long long INF = numeric_limits<long long>::max() / 4;
struct Edge {
    int destination;
    long long weight;
};

vector<long long> shortest_distances(const vector<vector<Edge>>& graph, int source) {
    vector<long long> distance(graph.size(), INF);
    using Entry = pair<long long, int>;
    priority_queue<Entry, vector<Entry>, greater<Entry>> pending;
    distance[source] = 0;
    pending.push({0, source});
    while (!pending.empty()) {
        auto [current_distance, vertex] = pending.top();
        pending.pop();
        if (current_distance != distance[vertex]) {
            continue;
        }
        for (const Edge& edge : graph[vertex]) {
            long long candidate = current_distance + edge.weight;
            if (candidate < distance[edge.destination]) {
                distance[edge.destination] = candidate;
                pending.push({candidate, edge.destination});
            }
        }
    }
    return distance;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    vector<vector<Edge>> graph(vertex_count + 1);
    for (int index = 0; index < edge_count; ++index) {
        int first, second;
        long long weight;
        cin >> first >> second >> weight;
        graph[first].push_back({second, weight});
    }
    vector<long long> distance = shortest_distances(graph, 1);
    for (int vertex = 1; vertex <= vertex_count; ++vertex) {
        cout << (distance[vertex] == INF ? -1 : distance[vertex])
             << (vertex == vertex_count ? '\n' : ' ');
    }
}

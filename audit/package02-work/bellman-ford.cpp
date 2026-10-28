#include <bits/stdc++.h>
using namespace std;

constexpr long long INF = numeric_limits<long long>::max() / 4;
struct Edge {
    int from, to;
    long long weight;
};
struct Result {
    vector<long long> distance;
    vector<bool> unbounded;
};

Result shortest_paths(int vertex_count, const vector<Edge>& edges, int source) {
    vector<vector<int>> graph(vertex_count + 1);
    for (const Edge& edge : edges) {
        graph[edge.from].push_back(edge.to);
    }
    Result result{vector<long long>(vertex_count + 1, INF),
                  vector<bool>(vertex_count + 1)};
    result.distance[source] = 0;
    for (int pass = 1; pass < vertex_count; ++pass) {
        bool changed = false;
        for (const Edge& edge : edges) {
            if (result.distance[edge.from] == INF) {
                continue;
            }
            long long candidate = result.distance[edge.from] + edge.weight;
            if (candidate < result.distance[edge.to]) {
                result.distance[edge.to] = candidate;
                changed = true;
            }
        }
        if (!changed) {
            break;
        }
    }
    queue<int> pending;
    for (const Edge& edge : edges) {
        if (result.distance[edge.from] != INF &&
            result.distance[edge.from] + edge.weight < result.distance[edge.to] &&
            !result.unbounded[edge.to]) {
            result.unbounded[edge.to] = true;
            pending.push(edge.to);
        }
    }
    while (!pending.empty()) {
        int vertex = pending.front();
        pending.pop();
        for (int next : graph[vertex]) {
            if (!result.unbounded[next]) {
                result.unbounded[next] = true;
                pending.push(next);
            }
        }
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    vector<Edge> edges(edge_count);
    for (Edge& edge : edges) {
        cin >> edge.from >> edge.to >> edge.weight;
    }
    Result result = shortest_paths(vertex_count, edges, 1);
    for (int vertex = 1; vertex <= vertex_count; ++vertex) {
        if (result.unbounded[vertex]) {
            cout << "-INF";
        } else if (result.distance[vertex] == INF) {
            cout << "UNREACHABLE";
        } else {
            cout << result.distance[vertex];
        }
        cout << (vertex == vertex_count ? '\n' : ' ');
    }
}

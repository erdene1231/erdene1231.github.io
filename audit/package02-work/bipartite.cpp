#include <bits/stdc++.h>
using namespace std;

optional<vector<int>> two_color(const vector<vector<int>>& graph) {
    int count = static_cast<int>(graph.size()) - 1;
    vector<int> color(count + 1);
    queue<int> pending;
    for (int start = 1; start <= count; ++start) {
        if (color[start] != 0) {
            continue;
        }
        color[start] = 1;
        pending.push(start);
        while (!pending.empty()) {
            int vertex = pending.front();
            pending.pop();
            for (int next : graph[vertex]) {
                if (color[next] == 0) {
                    color[next] = 3 - color[vertex];
                    pending.push(next);
                } else if (color[next] == color[vertex]) {
                    return nullopt;
                }
            }
        }
    }
    return color;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    vector<vector<int>> graph(vertex_count + 1);
    for (int edge = 0; edge < edge_count; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }
    auto color = two_color(graph);
    if (!color.has_value()) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    for (int vertex = 1; vertex <= vertex_count; ++vertex) {
        cout << (*color)[vertex] << (vertex == vertex_count ? '\n' : ' ');
    }
}

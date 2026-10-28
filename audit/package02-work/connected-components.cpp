#include <bits/stdc++.h>
using namespace std;

struct Components {
    vector<int> label;
    vector<int> representatives;
};

Components find_components(const vector<vector<int>>& graph) {
    int count = static_cast<int>(graph.size()) - 1;
    Components result{vector<int>(count + 1), {}};
    queue<int> pending;
    for (int start = 1; start <= count; ++start) {
        if (result.label[start] != 0) {
            continue;
        }
        result.representatives.push_back(start);
        int component = static_cast<int>(result.representatives.size());
        result.label[start] = component;
        pending.push(start);
        while (!pending.empty()) {
            int vertex = pending.front();
            pending.pop();
            for (int next : graph[vertex]) {
                if (result.label[next] == 0) {
                    result.label[next] = component;
                    pending.push(next);
                }
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
    vector<vector<int>> graph(vertex_count + 1);
    for (int edge = 0; edge < edge_count; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }
    Components result = find_components(graph);
    cout << result.representatives.size() - 1 << '\n';
    for (int index = 1; index < static_cast<int>(result.representatives.size()); ++index) {
        cout << result.representatives[0] << ' ' << result.representatives[index] << '\n';
    }
}

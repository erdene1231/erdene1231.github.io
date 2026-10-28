#include <bits/stdc++.h>
using namespace std;

struct AncestorTable {
    int levels = 1;
    vector<int> depth;
    vector<vector<int>> up;

    explicit AncestorTable(const vector<vector<int>>& graph) {
        int count = static_cast<int>(graph.size()) - 1;
        while ((1LL << levels) <= count) {
            ++levels;
        }
        depth.assign(count + 1, -1);
        up.assign(levels, vector<int>(count + 1, 0));
        queue<int> pending;
        depth[1] = 0;
        pending.push(1);
        while (!pending.empty()) {
            int vertex = pending.front();
            pending.pop();
            for (int next : graph[vertex]) {
                if (depth[next] != -1) {
                    continue;
                }
                depth[next] = depth[vertex] + 1;
                up[0][next] = vertex;
                pending.push(next);
            }
        }
        for (int level = 1; level < levels; ++level) {
            for (int vertex = 1; vertex <= count; ++vertex) {
                up[level][vertex] = up[level - 1][up[level - 1][vertex]];
            }
        }
    }

    int climb(int vertex, int steps) const {
        for (int level = 0; level < levels; ++level) {
            if ((steps >> level) & 1) {
                vertex = up[level][vertex];
            }
        }
        return vertex;
    }

    int lca(int first, int second) const {
        if (depth[first] < depth[second]) {
            swap(first, second);
        }
        first = climb(first, depth[first] - depth[second]);
        if (first == second) {
            return first;
        }
        for (int level = levels - 1; level >= 0; --level) {
            if (up[level][first] != up[level][second]) {
                first = up[level][first];
                second = up[level][second];
            }
        }
        return up[0][first];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count, query_count;
    cin >> count >> query_count;
    vector<vector<int>> graph(count + 1);
    for (int edge = 0; edge < count - 1; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }
    AncestorTable table(graph);
    for (int query = 0; query < query_count; ++query) {
        int first, second;
        cin >> first >> second;
        int ancestor = table.lca(first, second);
        int distance = table.depth[first] + table.depth[second] - 2 * table.depth[ancestor];
        cout << ancestor << ' ' << distance << '\n';
    }
}

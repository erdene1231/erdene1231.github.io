#include <bits/stdc++.h>
using namespace std;

constexpr long long MOD = 1000000007;

long long count_independent_sets(const vector<vector<int>>& graph) {
    int count = static_cast<int>(graph.size()) - 1;
    vector<int> parent(count + 1), order, pending{1};
    order.reserve(count);
    while (!pending.empty()) {
        int vertex = pending.back();
        pending.pop_back();
        order.push_back(vertex);
        for (int next : graph[vertex]) {
            if (next != parent[vertex]) {
                parent[next] = vertex;
                pending.push_back(next);
            }
        }
    }
    vector<long long> omitted(count + 1, 1), selected(count + 1, 1);
    for (int index = count - 1; index >= 0; --index) {
        int vertex = order[index];
        for (int child : graph[vertex]) {
            if (child == parent[vertex]) {
                continue;
            }
            omitted[vertex] = omitted[vertex]
                * ((omitted[child] + selected[child]) % MOD) % MOD;
            selected[vertex] = selected[vertex] * omitted[child] % MOD;
        }
    }
    return (omitted[1] + selected[1]) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count;
    cin >> count;
    vector<vector<int>> graph(count + 1);
    for (int edge = 0; edge < count - 1; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }
    cout << count_independent_sets(graph) << '\n';
}

#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int from, to;
    long long weight;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<Edge> edges(m);
    for (auto& edge : edges) {
        cin >> edge.from >> edge.to >> edge.weight;
        edge.from--;
        edge.to--;
    }

    const long long INF = LLONG_MAX / 4;
    vector<long long> dist(n, INF);
    dist[0] = 0;
    for (int pass = 0; pass < n; pass++) {
        bool changed = false;
        for (const auto& edge : edges) {
            if (dist[edge.from] == INF) {
                continue;
            }
            long long candidate = dist[edge.from] + edge.weight;
            if (candidate < dist[edge.to]) {
                dist[edge.to] = candidate;
                changed = true;
            }
        }
        if (!changed) {
            break;
        }
        if (pass == n - 1) {
            cout << "NEGATIVE CYCLE\n";
            return 0;
        }
    }

    for (int i = 0; i < n; i++) {
        if (i > 0) {
            cout << ' ';
        }
        if (dist[i] == INF) {
            cout << "INF";
        } else {
            cout << dist[i];
        }
    }
    cout << '\n';
    return 0;
}

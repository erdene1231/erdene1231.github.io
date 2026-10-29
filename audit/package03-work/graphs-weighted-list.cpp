#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Graph {
    int n;
    bool dir;
    vector<vector<pair<int, ll>>> adj;
    Graph(int _n, bool _dir) {
        n = _n;
        dir = _dir;
        adj.resize(n + 1);
    }
    void add(int a, int b, ll w) {
        adj[a].push_back({b, w});
        if (!dir) adj[b].push_back({a, w});
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir;
    cin >> n >> m >> dir;
    Graph g(n, dir);
    for (int i = 0; i < m; i++) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        g.add(a, b, w);
    }
    for (int u = 1; u <= n; u++) {
        cout << u << ':';
        for (auto [v, w] : g.adj[u]) cout << ' ' << v << ':' << w;
        cout << '\n';
    }
}

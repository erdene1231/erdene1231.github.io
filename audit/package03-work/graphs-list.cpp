#include <bits/stdc++.h>
using namespace std;

struct Graph {
    int n;
    bool dir;
    vector<vector<int>> adj;
    vector<int> in, out;
    Graph(int _n, bool _dir) {
        n = _n;
        dir = _dir;
        adj.resize(n + 1);
        in.resize(n + 1);
        out.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        out[a]++;
        in[b]++;
        if (!dir) {
            adj[b].push_back(a);
            out[b]++;
            in[a]++;
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir;
    cin >> n >> m >> dir;
    Graph g(n, dir);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    for (int u = 1; u <= n; u++) {
        cout << u << ':';
        for (int v : g.adj[u]) cout << ' ' << v;
        cout << '\n';
    }
    for (int u = 1; u <= n; u++) cout << g.in[u] << (u == n ? '\n' : ' ');
    for (int u = 1; u <= n; u++) cout << g.out[u] << (u == n ? '\n' : ' ');
}

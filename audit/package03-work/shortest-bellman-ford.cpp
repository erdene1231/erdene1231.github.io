#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 4'000'000'000'000'000'000LL;

struct Graph {
    int n;
    vector<tuple<int, int, ll>> edges;
    vector<vector<int>> adj;
    vector<ll> dist;
    vector<int> bad;
    Graph(int _n) {
        n = _n;
        adj.resize(n + 1);
    }
    void add(int a, int b, ll w) {
        edges.push_back({a, b, w});
        adj[a].push_back(b);
    }
    void run(int s) {
        dist.assign(n + 1, INF);
        bad.assign(n + 1, 0);
        dist[s] = 0;
        for (int i = 1; i <= n; i++) {
            bool changed = false;
            for (auto [a, b, w] : edges) {
                if (dist[a] == INF) continue;
                if (dist[a] + w < dist[b]) {
                    dist[b] = dist[a] + w;
                    changed = true;
                    if (i == n) bad[b] = 1;
                }
            }
            if (!changed) break;
        }
        queue<int> q;
        for (int u = 1; u <= n; u++) if (bad[u]) q.push(u);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (int v : adj[u]) {
                if (bad[v]) continue;
                bad[v] = 1;
                q.push(v);
            }
        }
    }
    bool anyNegativeCycle() {
        vector<ll> d(n + 1, 0);
        for (int i = 1; i <= n; i++) {
            bool changed = false;
            for (auto [a, b, w] : edges) {
                if (d[a] + w < d[b]) {
                    d[b] = d[a] + w;
                    changed = true;
                }
            }
            if (!changed) return false;
        }
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir, s;
    cin >> n >> m >> dir >> s;
    Graph g(n);
    for (int i = 0; i < m; i++) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        g.add(a, b, w);
        if (!dir) g.add(b, a, w);
    }
    g.run(s);
    for (int u = 1; u <= n; u++) {
        if (g.bad[u]) cout << "-INF";
        else if (g.dist[u] == INF) cout << "INF";
        else cout << g.dist[u];
        cout << (u == n ? '\n' : ' ');
    }
    cout << (g.anyNegativeCycle() ? "GLOBAL_NEGATIVE_CYCLE" : "NO_NEGATIVE_CYCLE") << '\n';
}

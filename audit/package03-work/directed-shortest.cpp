#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s;
    cin >> n >> m >> s;
    vector<vector<pair<int, ll>>> adj(n + 1);
    for (int i = 0, a, b; i < m; i++) {
        ll w;
        cin >> a >> b >> w;
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    }
    const ll INF = 1LL << 62;
    vector<ll> dist(n + 1, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> q;
    dist[s] = 0;
    q.push({0, s});
    while (!q.empty()) {
        auto [d, u] = q.top();
        q.pop();
        if (d != dist[u]) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[v] > d + w) {
                dist[v] = d + w;
                q.push({dist[v], v});
            }
        }
    }
    vector<int> ord(n);
    iota(ord.begin(), ord.end(), 1);
    sort(ord.begin(), ord.end(), [&](int a, int b) {
        return dist[a] < dist[b];
    });
    vector<ll> ways(n + 1);
    ways[s] = 1;
    for (int u : ord) {
        if (dist[u] == INF) continue;
        for (auto [v, w] : adj[u]) {
            if (dist[u] + w == dist[v]) ways[v] += ways[u];
        }
    }
    for (int u = 1; u <= n; u++) {
        if (dist[u] == INF) cout << "INF 0\n";
        else cout << dist[u] << ' ' << ways[u] << '\n';
    }
}

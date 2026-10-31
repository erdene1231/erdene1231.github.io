#include <bits/stdc++.h>
using namespace std;
using ll = long long;
using Edge = pair<int, int>;

vector<ll> dijkstra(const vector<vector<Edge>> &g, int start) {
    const ll inf = 1LL << 60;
    vector<ll> dist(g.size(), inf);
    using State = pair<ll, int>;
    priority_queue<State, vector<State>, greater<State>> q;
    dist[start] = 0;
    q.push({0, start});
    while (!q.empty()) {
        auto [du, u] = q.top();
        q.pop();
        if (du != dist[u]) continue;
        for (auto [v, w] : g[u]) {
            if (du + w < dist[v]) {
                dist[v] = du + w;
                q.push({dist[v], v});
            }
        }
    }
    return dist;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<Edge>> g(n);
    for (int i = 0; i < m; ++i) {
        int a, b, c;
        cin >> a >> b >> c;
        --a;
        --b;
        g[a].push_back({b, c});
        g[b].push_back({a, c});
    }
    auto d1 = dijkstra(g, 0);
    auto dn = dijkstra(g, n - 1);
    for (int k = 0; k < n; ++k) cout << d1[k] + dn[k] << '\n';
}

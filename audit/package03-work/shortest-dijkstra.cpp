#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 4'000'000'000'000'000'000LL;

struct Graph {
    int n;
    vector<vector<pair<int, ll>>> adj;
    vector<ll> dist;
    vector<int> par;
    Graph(int _n) {
        n = _n;
        adj.resize(n + 1);
    }
    void add(int a, int b, ll w) {
        adj[a].push_back({b, w});
    }
    void run(int s) {
        dist.assign(n + 1, INF);
        par.assign(n + 1, -1);
        using P = pair<ll, int>;
        priority_queue<P, vector<P>, greater<P>> q;
        dist[s] = 0;
        q.push({0, s});
        while (!q.empty()) {
            auto [d, u] = q.top();
            q.pop();
            if (d != dist[u]) continue;
            for (auto [v, w] : adj[u]) {
                if (d + w < dist[v]) {
                    dist[v] = d + w;
                    par[v] = u;
                    q.push({dist[v], v});
                }
            }
        }
    }
    vector<int> path(int t) {
        if (dist[t] == INF) return {};
        vector<int> res;
        while (t != -1) {
            res.push_back(t);
            t = par[t];
        }
        reverse(res.begin(), res.end());
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir, s, t;
    cin >> n >> m >> dir >> s >> t;
    Graph g(n);
    bool negative = false;
    for (int i = 0; i < m; i++) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        negative |= w < 0;
        g.add(a, b, w);
        if (!dir) g.add(b, a, w);
    }
    if (negative) {
        cout << "NEGATIVE_EDGE\n";
        return 0;
    }
    g.run(s);
    for (int u = 1; u <= n; u++) {
        if (g.dist[u] == INF) cout << "INF";
        else cout << g.dist[u];
        cout << (u == n ? '\n' : ' ');
    }
    auto path = g.path(t);
    if (path.empty()) cout << "IMPOSSIBLE\n";
    else for (int i = 0; i < (int)path.size(); i++) {
        cout << path[i] << (i + 1 == (int)path.size() ? '\n' : ' ');
    }
}

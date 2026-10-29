#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 4'000'000'000'000'000'000LL;

struct Graph {
    int n;
    vector<vector<pair<int, ll>>> adj;
    vector<ll> dist;
    Graph(int _n) {
        n = _n;
        adj.resize(n + 1);
    }
    void add(int a, int b, ll w) {
        adj[a].push_back({b, w});
    }
    bool run(int s) {
        dist.assign(n + 1, INF);
        vector<int> inq(n + 1), len(n + 1);
        queue<int> q;
        dist[s] = 0;
        q.push(s);
        inq[s] = 1;
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            inq[u] = 0;
            for (auto [v, w] : adj[u]) {
                if (dist[u] + w >= dist[v]) continue;
                dist[v] = dist[u] + w;
                len[v] = len[u] + 1;
                if (len[v] >= n) return false;
                if (!inq[v]) {
                    inq[v] = 1;
                    q.push(v);
                }
            }
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
    if (!g.run(s)) {
        cout << "REACHABLE_NEGATIVE_CYCLE\n";
        return 0;
    }
    for (int u = 1; u <= n; u++) {
        if (g.dist[u] == INF) cout << "INF";
        else cout << g.dist[u];
        cout << (u == n ? '\n' : ' ');
    }
}

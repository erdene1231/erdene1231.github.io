#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = 4'000'000'000'000'000'000LL;

struct Graph {
    int n;
    vector<vector<ll>> dist;
    vector<vector<int>> bad;
    Graph(int _n) {
        n = _n;
        dist.assign(n + 1, vector<ll>(n + 1, INF));
        for (int u = 1; u <= n; u++) dist[u][u] = 0;
    }
    void add(int a, int b, ll w) {
        dist[a][b] = min(dist[a][b], w);
    }
    void run() {
        for (int k = 1; k <= n; k++) {
            for (int i = 1; i <= n; i++) {
                if (dist[i][k] == INF) continue;
                for (int j = 1; j <= n; j++) {
                    if (dist[k][j] == INF) continue;
                    ll d = max(-INF, dist[i][k] + dist[k][j]);
                    dist[i][j] = min(dist[i][j], d);
                }
            }
        }
        bad.assign(n + 1, vector<int>(n + 1));
        for (int k = 1; k <= n; k++) {
            if (dist[k][k] >= 0) continue;
            for (int i = 1; i <= n; i++) {
                for (int j = 1; j <= n; j++) {
                    if (dist[i][k] != INF && dist[k][j] != INF) bad[i][j] = 1;
                }
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir;
    cin >> n >> m >> dir;
    Graph g(n);
    for (int i = 0; i < m; i++) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        g.add(a, b, w);
        if (!dir) g.add(b, a, w);
    }
    g.run();
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (g.bad[i][j]) cout << "-INF";
            else if (g.dist[i][j] == INF) cout << "INF";
            else cout << g.dist[i][j];
            cout << (j == n ? '\n' : ' ');
        }
    }
}

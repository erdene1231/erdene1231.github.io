#include <bits/stdc++.h>
using namespace std;

struct Graph {
    int n;
    bool dir;
    vector<vector<int>> adj;
    vector<int> dist, par, ord;
    Graph(int _n, bool _dir) {
        n = _n;
        dir = _dir;
        adj.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        if (!dir) adj[b].push_back(a);
    }
    void bfs(int s) {
        dist.assign(n + 1, -1);
        par.assign(n + 1, -1);
        ord.clear();
        queue<int> q;
        dist[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            ord.push_back(u);
            for (int v : adj[u]) {
                if (dist[v] != -1) continue;
                dist[v] = dist[u] + 1;
                par[v] = u;
                q.push(v);
            }
        }
    }
    vector<int> path(int t) {
        if (dist[t] == -1) return {};
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
    Graph g(n, dir);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.bfs(s);
    for (int i = 0; i < (int)g.ord.size(); i++) {
        cout << g.ord[i] << (i + 1 == (int)g.ord.size() ? '\n' : ' ');
    }
    for (int u = 1; u <= n; u++) cout << g.dist[u] << (u == n ? '\n' : ' ');
    auto path = g.path(t);
    if (path.empty()) cout << "IMPOSSIBLE\n";
    else for (int i = 0; i < (int)path.size(); i++) {
        cout << path[i] << (i + 1 == (int)path.size() ? '\n' : ' ');
    }
}

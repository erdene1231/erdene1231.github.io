#include <bits/stdc++.h>
using namespace std;

struct Lowlink {
    int n, timer = 0;
    vector<vector<pair<int, int>>> adj;
    vector<pair<int, int>> edges;
    vector<int> tin, low, par, pe, it, child, cut, bridge;
    Lowlink(int _n) {
        n = _n;
        adj.resize(n + 1);
    }
    void add(int u, int v) {
        int id = (int)edges.size();
        edges.push_back({u, v});
        adj[u].push_back({v, id});
        adj[v].push_back({u, id});
    }
    void run() {
        timer = 0;
        tin.assign(n + 1, 0);
        low.assign(n + 1, 0);
        par.assign(n + 1, 0);
        pe.assign(n + 1, -1);
        it.assign(n + 1, 0);
        child.assign(n + 1, 0);
        cut.assign(n + 1, 0);
        bridge.assign(edges.size(), 0);
        for (int r = 1; r <= n; r++) {
            if (tin[r]) continue;
            vector<int> st = {r};
            tin[r] = low[r] = ++timer;
            while (!st.empty()) {
                int u = st.back();
                if (it[u] < (int)adj[u].size()) {
                    auto [v, id] = adj[u][it[u]++];
                    if (id == pe[u]) continue;
                    if (!tin[v]) {
                        par[v] = u;
                        pe[v] = id;
                        child[u]++;
                        tin[v] = low[v] = ++timer;
                        st.push_back(v);
                    } else {
                        low[u] = min(low[u], tin[v]);
                    }
                } else {
                    st.pop_back();
                    int p = par[u];
                    if (!p) {
                        cut[u] = child[u] > 1;
                    } else {
                        low[p] = min(low[p], low[u]);
                        if (low[u] > tin[p]) bridge[pe[u]] = 1;
                        if (par[p] && low[u] >= tin[p]) cut[p] = 1;
                    }
                }
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    Lowlink g(n);
    for (int i = 0, u, v; i < m; i++) {
        cin >> u >> v;
        g.add(u, v);
    }
    g.run();
    vector<int> b, c;
    for (int i = 0; i < m; i++) if (g.bridge[i]) b.push_back(i + 1);
    for (int u = 1; u <= n; u++) if (g.cut[u]) c.push_back(u);
    cout << b.size() << '\n';
    for (int id : b) cout << id << ' ';
    cout << '\n' << c.size() << '\n';
    for (int u : c) cout << u << ' ';
    cout << '\n';
}

#include <bits/stdc++.h>
using namespace std;

struct Centroid {
    static constexpr int INF = 1000000000;
    int n;
    vector<vector<int>> adj;
    vector<vector<pair<int, int>>> path;
    vector<int> par, sz, cdpar, best;
    vector<char> blocked;
    Centroid(int _n) {
        n = _n;
        adj.resize(n + 1);
        path.resize(n + 1);
        par.resize(n + 1);
        sz.resize(n + 1);
        cdpar.resize(n + 1);
        best.assign(n + 1, INF);
        blocked.resize(n + 1);
    }
    void add(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    int find(int start) {
        vector<int> order = {start};
        par[start] = 0;
        for (int i = 0; i < (int)order.size(); i++) {
            int u = order[i];
            for (int v : adj[u]) {
                if (blocked[v] || v == par[u]) continue;
                par[v] = u;
                order.push_back(v);
            }
        }
        for (int i = (int)order.size() - 1; i >= 0; i--) {
            int u = order[i];
            sz[u] = 1;
            for (int v : adj[u]) {
                if (!blocked[v] && par[v] == u) sz[u] += sz[v];
            }
        }
        int cnt = (int)order.size();
        for (int u : order) {
            int mx = cnt - sz[u];
            for (int v : adj[u]) {
                if (!blocked[v] && par[v] == u) mx = max(mx, sz[v]);
            }
            if (mx <= cnt / 2) return u;
        }
        return start;
    }
    void decompose(int start, int p) {
        int c = find(start);
        cdpar[c] = p;
        {
            vector<tuple<int, int, int>> st = {{c, 0, 0}};
            while (!st.empty()) {
                auto [u, prev, d] = st.back();
                st.pop_back();
                path[u].push_back({c, d});
                for (int v : adj[u]) {
                    if (!blocked[v] && v != prev) st.push_back({v, u, d + 1});
                }
            }
        }
        blocked[c] = true;
        for (int v : adj[c]) {
            if (!blocked[v]) decompose(v, c);
        }
    }
    void build() {
        fill(blocked.begin(), blocked.end(), false);
        fill(cdpar.begin(), cdpar.end(), 0);
        fill(best.begin(), best.end(), INF);
        for (auto& a : path) a.clear();
        decompose(1, 0);
    }
    void mark(int u) {
        for (auto [c, d] : path[u]) best[c] = min(best[c], d);
    }
    int query(int u) {
        int ans = INF;
        for (auto [c, d] : path[u]) {
            if (best[c] != INF) ans = min(ans, d + best[c]);
        }
        return ans == INF ? -1 : ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    Centroid cd(n);
    for (int i = 1, u, v; i < n; i++) {
        cin >> u >> v;
        cd.add(u, v);
    }
    cd.build();
    cd.mark(1);
    while (q--) {
        int type, u;
        cin >> type >> u;
        if (type == 1) cd.mark(u);
        else cout << cd.query(u) << '\n';
    }
}

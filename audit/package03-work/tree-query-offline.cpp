#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DSU {
    vector<int> par, sz;
    DSU(int n) {
        par.resize(n + 1);
        iota(par.begin(), par.end(), 0);
        sz.assign(n + 1, 1);
    }
    int find(int u) {
        return par[u] == u ? u : par[u] = find(par[u]);
    }
    void unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return;
        if (sz[a] < sz[b]) swap(a, b);
        par[b] = a;
        sz[a] += sz[b];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, root;
    cin >> n >> q >> root;
    vector<vector<int>> adj(n + 1);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    vector<vector<pair<int, int>>> queries(n + 1);
    for (int i = 0, a, b; i < q; i++) {
        cin >> a >> b;
        queries[a].push_back({b, i});
        if (a != b) queries[b].push_back({a, i});
    }
    DSU d(n);
    vector<int> top(n + 1), seen(n + 1), ans(q);
    iota(top.begin(), top.end(), 0);
    auto enter = [&](int u) {
        seen[u] = true;
        for (auto [v, id] : queries[u]) {
            if (seen[v]) ans[id] = top[d.find(v)];
        }
    };
    vector<array<int, 3>> st = {{root, 0, 0}};
    enter(root);
    while (!st.empty()) {
        int u = st.back()[0], p = st.back()[1];
        int &i = st.back()[2];
        if (i == (int)adj[u].size()) {
            st.pop_back();
            if (p != 0) {
                d.unite(p, u);
                top[d.find(p)] = p;
            }
            continue;
        }
        int v = adj[u][i++];
        if (v == p) continue;
        st.push_back({v, u, 0});
        enter(v);
    }
    for (int x : ans) cout << x << '\n';
}

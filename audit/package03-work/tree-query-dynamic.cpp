#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct TreeOrder {
    int n;
    vector<vector<int>> adj;
    vector<int> par, tin, sz, ord;
    TreeOrder(int _n) {
        n = _n;
        adj.resize(n + 1);
        par.resize(n + 1);
        tin.resize(n + 1);
        sz.assign(n + 1, 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    void build(int root) {
        vector<int> st = {root};
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            tin[u] = (int)ord.size() + 1;
            ord.push_back(u);
            for (int i = (int)adj[u].size() - 1; i >= 0; i--) {
                int v = adj[u][i];
                if (v == par[u]) continue;
                par[v] = u;
                st.push_back(v);
            }
        }
        for (int i = n - 1; i > 0; i--) sz[par[ord[i]]] += sz[ord[i]];
    }
};

struct Fenwick {
    int n;
    vector<ll> bit;
    Fenwick(int _n) {
        n = _n;
        bit.resize(n + 1);
    }
    void add(int i, ll x) {
        for (; i <= n; i += i & -i) bit[i] += x;
    }
    ll sum(int i) const {
        ll ans = 0;
        for (; i > 0; i -= i & -i) ans += bit[i];
        return ans;
    }
    ll range(int l, int r) const {
        return sum(r) - sum(l - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, root;
    cin >> n >> q >> root;
    vector<ll> val(n + 1);
    for (int u = 1; u <= n; u++) cin >> val[u];
    TreeOrder g(n);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.build(root);
    Fenwick sub(n), path(n);
    auto change = [&](int u, ll d) {
        int l = g.tin[u], r = l + g.sz[u] - 1;
        sub.add(l, d);
        path.add(l, d);
        if (r < n) path.add(r + 1, -d);
    };
    for (int u = 1; u <= n; u++) change(u, val[u]);
    while (q--) {
        char type;
        int u;
        cin >> type >> u;
        if (type == 'U') {
            ll x;
            cin >> x;
            change(u, x - val[u]);
            val[u] = x;
        } else if (type == 'T') cout << sub.range(g.tin[u], g.tin[u] + g.sz[u] - 1) << '\n';
        else cout << path.sum(g.tin[u]) << '\n';
    }
}

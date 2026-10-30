#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Segtree {
    int n;
    vector<ll> t;
    Segtree(int _n) {
        n = _n;
        t.resize(4 * n + 5);
    }
    void build(int v, int tl, int tr, const vector<ll>& a) {
        if (tl == tr) {
            t[v] = a[tl];
            return;
        }
        int tm = tl + (tr - tl) / 2;
        build(v * 2, tl, tm, a);
        build(v * 2 + 1, tm + 1, tr, a);
        t[v] = t[v * 2] + t[v * 2 + 1];
    }
    void update(int v, int tl, int tr, int p, ll x) {
        if (tl == tr) {
            t[v] = x;
            return;
        }
        int tm = tl + (tr - tl) / 2;
        if (p <= tm) update(v * 2, tl, tm, p, x);
        else update(v * 2 + 1, tm + 1, tr, p, x);
        t[v] = t[v * 2] + t[v * 2 + 1];
    }
    ll query(int v, int tl, int tr, int l, int r) {
        if (l > r) return 0;
        if (l == tl && r == tr) return t[v];
        int tm = tl + (tr - tl) / 2;
        return query(v * 2, tl, tm, l, min(r, tm))
             + query(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r);
    }
};

struct HLD {
    int n, timer = 0;
    vector<vector<int>> adj;
    vector<int> par, dep, sz, heavy, head, pos;
    HLD(int _n) {
        n = _n;
        adj.resize(n + 1);
        par.resize(n + 1);
        dep.resize(n + 1);
        sz.resize(n + 1);
        heavy.resize(n + 1);
        head.resize(n + 1);
        pos.resize(n + 1);
    }
    void add(int u, int v) {
        adj[u].push_back(v);
        adj[v].push_back(u);
    }
    void build() {
        timer = 0;
        fill(par.begin(), par.end(), 0);
        fill(dep.begin(), dep.end(), 0);
        fill(sz.begin(), sz.end(), 1);
        fill(heavy.begin(), heavy.end(), 0);
        vector<int> order = {1};
        for (int i = 0; i < n; i++) {
            int u = order[i];
            for (int v : adj[u]) {
                if (v == par[u]) continue;
                par[v] = u;
                dep[v] = dep[u] + 1;
                order.push_back(v);
            }
        }
        for (int i = n - 1; i >= 0; i--) {
            int u = order[i];
            for (int v : adj[u]) {
                if (par[v] != u) continue;
                sz[u] += sz[v];
                if (!heavy[u] || sz[v] > sz[heavy[u]]) heavy[u] = v;
            }
        }
        vector<pair<int, int>> st = {{1, 1}};
        while (!st.empty()) {
            auto [u, h] = st.back();
            st.pop_back();
            for (; u; u = heavy[u]) {
                head[u] = h;
                pos[u] = ++timer;
                for (int v : adj[u]) {
                    if (par[v] == u && v != heavy[u]) st.push_back({v, v});
                }
            }
        }
    }
    ll path(int u, int v, Segtree& seg, bool edge) {
        ll ans = 0;
        while (head[u] != head[v]) {
            if (dep[head[u]] < dep[head[v]]) swap(u, v);
            ans += seg.query(1, 1, n, pos[head[u]], pos[u]);
            u = par[head[u]];
        }
        if (dep[u] > dep[v]) swap(u, v);
        return ans + seg.query(1, 1, n, pos[u] + edge, pos[v]);
    }
    ll subtree(int u, Segtree& seg, bool edge) {
        return seg.query(1, 1, n, pos[u] + edge, pos[u] + sz[u] - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    char mode;
    cin >> n >> q >> mode;
    bool edge = mode == 'E';
    vector<ll> a(n + 1), b(n + 1);
    for (int u = 1; u <= n; u++) cin >> a[u];
    HLD hld(n);
    for (int i = 1, u, v; i < n; i++) {
        cin >> u >> v;
        hld.add(u, v);
    }
    hld.build();
    for (int u = 1; u <= n; u++) b[hld.pos[u]] = a[u];
    Segtree seg(n);
    seg.build(1, 1, n, b);
    while (q--) {
        int type, u;
        cin >> type >> u;
        if (type == 1) {
            ll x;
            cin >> x;
            seg.update(1, 1, n, hld.pos[u], x);
        } else if (type == 2) {
            int v;
            cin >> v;
            cout << hld.path(u, v, seg, edge) << '\n';
        } else {
            cout << hld.subtree(u, seg, edge) << '\n';
        }
    }
}

#include <bits/stdc++.h>
using namespace std;

struct Tree {
    int n, diam;
    vector<vector<int>> adj;
    vector<int> par, dep, ord, sz, down, up, first, second, who;
    Tree(int _n) {
        n = _n;
        adj.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    void root(int r) {
        par.assign(n + 1, 0);
        dep.assign(n + 1, 0);
        ord = {r};
        for (int i = 0; i < (int)ord.size(); i++) {
            int u = ord[i];
            for (int v : adj[u]) {
                if (v == par[u]) continue;
                par[v] = u;
                dep[v] = dep[u] + 1;
                ord.push_back(v);
            }
        }
    }
    void dp() {
        sz.assign(n + 1, 1);
        down.assign(n + 1, 0);
        first.assign(n + 1, 0);
        second.assign(n + 1, 0);
        who.assign(n + 1, 0);
        diam = 0;
        for (int i = n - 1; i >= 0; i--) {
            int u = ord[i];
            for (int v : adj[u]) {
                if (par[v] != u) continue;
                sz[u] += sz[v];
                int d = down[v] + 1;
                if (d > first[u]) {
                    second[u] = first[u];
                    first[u] = d;
                    who[u] = v;
                } else if (d > second[u]) second[u] = d;
            }
            down[u] = first[u];
            diam = max(diam, first[u] + second[u]);
        }
    }
    vector<int> dist(int s) {
        vector<int> d(n + 1, -1), st = {s};
        d[s] = 0;
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            for (int v : adj[u]) {
                if (d[v] != -1) continue;
                d[v] = d[u] + 1;
                st.push_back(v);
            }
        }
        return d;
    }
    tuple<int, int, int> diameter() {
        auto d = dist(1);
        int b = int(max_element(d.begin() + 1, d.end()) - d.begin());
        d = dist(b);
        int c = int(max_element(d.begin() + 1, d.end()) - d.begin());
        return {b, c, d[c]};
    }
    void reroot() {
        up.assign(n + 1, 0);
        for (int u : ord) {
            for (int v : adj[u]) {
                if (par[v] != u) continue;
                int other = who[u] == v ? second[u] : first[u];
                up[v] = 1 + max(up[u], other);
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, root;
    cin >> n >> root;
    Tree g(n);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.root(root);
    g.dp();
    g.reroot();
    vector<int> ecc(n + 1);
    for (int u = 1; u <= n; u++) ecc[u] = max(g.down[u], g.up[u]);
    auto print = [&](const vector<int> &a) {
        for (int u = 1; u <= n; u++) cout << a[u] << (u == n ? '\n' : ' ');
    };
    print(g.par);
    print(g.dep);
    print(g.sz);
    print(g.down);
    print(ecc);
    auto [b, c, d] = g.diameter();
    cout << g.diam << ' ' << d << ' ' << b << ' ' << c << '\n';
}

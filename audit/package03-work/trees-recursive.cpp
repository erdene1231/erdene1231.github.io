#include <bits/stdc++.h>
using namespace std;

struct Tree {
    int n;
    vector<vector<int>> adj;
    vector<int> par, dep, sz, ord;
    Tree(int _n) {
        n = _n;
        adj.resize(n + 1);
        par.resize(n + 1);
        dep.resize(n + 1);
        sz.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    void dfs(int u, int p) {
        par[u] = p;
        sz[u] = 1;
        ord.push_back(u);
        for (int v : adj[u]) {
            if (v == p) continue;
            dep[v] = dep[u] + 1;
            dfs(v, u);
            sz[u] += sz[v];
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
    g.dfs(root, 0);
    for (int u : g.ord) cout << u << ' ';
    cout << '\n';
    auto print = [&](const vector<int> &a) {
        for (int u = 1; u <= n; u++) cout << a[u] << (u == n ? '\n' : ' ');
    };
    print(g.par);
    print(g.dep);
    print(g.sz);
}

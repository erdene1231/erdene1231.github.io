#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DSU {
    vector<int> par, sz;
    DSU(int n) {
        par.resize(n + 1);
        sz.assign(n + 1, 1);
        iota(par.begin(), par.end(), 0);
    }
    int find(int u) {
        if (par[u] == u) return u;
        return par[u] = find(par[u]);
    }
    bool same(int a, int b) {
        return find(a) == find(b);
    }
    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        par[b] = a;
        sz[a] += sz[b];
        return true;
    }
};

struct Edge {
    int a, b;
    ll w;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<Edge> edges(m);
    for (auto &[a, b, w] : edges) cin >> a >> b >> w;
    sort(edges.begin(), edges.end(), [](const Edge &a, const Edge &b) {
        return a.w < b.w;
    });
    DSU d(n);
    ll sum = 0;
    vector<Edge> tree;
    for (auto e : edges) {
        if (!d.unite(e.a, e.b)) continue;
        sum += e.w;
        tree.push_back(e);
    }
    if ((int)tree.size() != n - 1) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    cout << sum << '\n';
    for (auto [a, b, w] : tree) cout << a << ' ' << b << ' ' << w << '\n';
}

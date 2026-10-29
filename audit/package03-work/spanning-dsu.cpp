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

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    DSU d(n);
    while (q--) {
        int t, a, b;
        cin >> t >> a >> b;
        if (t == 1) d.unite(a, b);
        else cout << d.same(a, b) << '\n';
    }
}

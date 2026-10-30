#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> par, sz;
    int cnt, mx;
    DSU(int n) {
        par.resize(n + 1);
        iota(par.begin(), par.end(), 0);
        sz.assign(n + 1, 1);
        cnt = n;
        mx = 1;
    }
    int find(int v) {
        while (par[v] != v) {
            par[v] = par[par[v]];
            v = par[v];
        }
        return v;
    }
    bool same(int a, int b) {
        return find(a) == find(b);
    }
    int size(int v) {
        return sz[find(v)];
    }
    bool unite(int a, int b) {
        a = find(a);
        b = find(b);
        if (a == b) return false;
        if (sz[a] < sz[b]) swap(a, b);
        par[b] = a;
        sz[a] += sz[b];
        cnt--;
        mx = max(mx, sz[a]);
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    DSU d(n);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        d.unite(a, b);
        cout << d.cnt << ' ' << d.mx << '\n';
    }
}

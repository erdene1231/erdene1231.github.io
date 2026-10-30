#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct TreeDP {
    int n;
    vector<vector<int>> adj;
    vector<int> par, ord, sz, down, up, first, second, who, ecc;
    vector<ll> sum;
    TreeDP(int _n) {
        n = _n;
        adj.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    void run(int r) {
        par.assign(n + 1, 0);
        ord = {r};
        for (int i = 0; i < (int)ord.size(); i++) {
            int u = ord[i];
            for (int v : adj[u]) {
                if (v == par[u]) continue;
                par[v] = u;
                ord.push_back(v);
            }
        }
        sz.assign(n + 1, 1);
        down.assign(n + 1, 0);
        up.assign(n + 1, 0);
        first.assign(n + 1, 0);
        second.assign(n + 1, 0);
        who.assign(n + 1, 0);
        ecc.assign(n + 1, 0);
        sum.assign(n + 1, 0);
        for (int i = n - 1; i >= 0; i--) {
            int u = ord[i];
            for (int v : adj[u]) {
                if (v == par[u]) continue;
                sz[u] += sz[v];
                sum[u] += sum[v] + sz[v];
                int d = down[v] + 1;
                if (d > first[u]) {
                    second[u] = first[u];
                    first[u] = d;
                    who[u] = v;
                } else if (d > second[u]) {
                    second[u] = d;
                }
            }
            down[u] = first[u];
        }
        for (int u : ord) {
            ecc[u] = max(down[u], up[u]);
            for (int v : adj[u]) {
                if (v == par[u]) continue;
                int other = who[u] == v ? second[u] : first[u];
                up[v] = 1 + max(up[u], other);
                sum[v] = sum[u] + n - 2LL * sz[v];
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    TreeDP g(n);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.run(1);
    for (int u = 1; u <= n; u++) {
        cout << g.sz[u] << ' ' << g.down[u] << ' ' << g.up[u] << ' '
             << g.ecc[u] << ' ' << g.sum[u] << '\n';
    }
}

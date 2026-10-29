#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct BinaryJump {
    int n, lg;
    vector<vector<int>> adj, up;
    vector<int> dep;
    BinaryJump(int _n) {
        n = _n;
        lg = 1;
        while ((1LL << lg) <= n) lg++;
        adj.resize(n + 1);
        dep.assign(n + 1, -1);
        up.assign(lg, vector<int>(n + 1));
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    void build(int root) {
        vector<int> ord = {root};
        dep[root] = 0;
        for (int i = 0; i < (int)ord.size(); i++) {
            int u = ord[i];
            for (int v : adj[u]) {
                if (v == up[0][u]) continue;
                up[0][v] = u;
                dep[v] = dep[u] + 1;
                ord.push_back(v);
            }
        }
        for (int j = 1; j < lg; j++) {
            for (int u = 1; u <= n; u++) up[j][u] = up[j - 1][up[j - 1][u]];
        }
    }
    int kth(int u, ll k) const {
        if (k > dep[u]) return 0;
        for (int j = 0; j < lg; j++) if ((k >> j) & 1LL) u = up[j][u];
        return u;
    }
    int lca(int a, int b) const {
        if (dep[a] < dep[b]) swap(a, b);
        a = kth(a, dep[a] - dep[b]);
        if (a == b) return a;
        for (int j = lg - 1; j >= 0; j--) {
            if (up[j][a] != up[j][b]) {
                a = up[j][a];
                b = up[j][b];
            }
        }
        return up[0][a];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, root;
    cin >> n >> q >> root;
    BinaryJump g(n);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.build(root);
    while (q--) {
        char type;
        int a;
        cin >> type >> a;
        if (type == 'K') {
            ll k;
            cin >> k;
            cout << g.kth(a, k) << '\n';
        } else {
            int b;
            cin >> b;
            int c = g.lca(a, b);
            cout << c << ' ' << g.dep[a] + g.dep[b] - 2 * g.dep[c] << '\n';
        }
    }
}

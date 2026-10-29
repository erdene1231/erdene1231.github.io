#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll INF = 1LL << 62;
struct Info {
    ll mn = INF, mx = -INF, sum = 0;
};
Info join(Info a, Info b) {
    return {min(a.mn, b.mn), max(a.mx, b.mx), a.sum + b.sum};
}

struct PathJump {
    int n, lg;
    bool vertex;
    vector<vector<pair<int, ll>>> adj;
    vector<vector<int>> up;
    vector<vector<Info>> agg;
    vector<int> dep;
    vector<ll> value, pref;
    PathJump(int _n) {
        n = _n;
        lg = 1;
        while ((1LL << lg) <= n) lg++;
        adj.resize(n + 1);
        up.assign(lg, vector<int>(n + 1));
        agg.assign(lg, vector<Info>(n + 1));
        dep.assign(n + 1, -1);
        pref.resize(n + 1);
    }
    void add(int a, int b, ll w) {
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    }
    void build(int root, const vector<ll> &val, bool onVertices) {
        vertex = onVertices;
        value = val;
        vector<int> ord = {root};
        dep[root] = 0;
        pref[root] = vertex ? value[root] : 0;
        for (int i = 0; i < (int)ord.size(); i++) {
            int u = ord[i];
            for (auto [v, w] : adj[u]) {
                if (v == up[0][u]) continue;
                up[0][v] = u;
                dep[v] = dep[u] + 1;
                ll x = vertex ? value[v] : w;
                agg[0][v] = {x, x, x};
                pref[v] = pref[u] + x;
                ord.push_back(v);
            }
        }
        for (int j = 1; j < lg; j++) {
            for (int u = 1; u <= n; u++) {
                int v = up[j - 1][u];
                up[j][u] = up[j - 1][v];
                agg[j][u] = join(agg[j - 1][u], agg[j - 1][v]);
            }
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
    Info path(int a, int b) const {
        int c = lca(a, b);
        Info ans;
        for (int u : {a, b}) {
            int d = dep[u] - dep[c];
            for (int j = 0; j < lg; j++) {
                if ((d >> j) & 1) {
                    ans = join(ans, agg[j][u]);
                    u = up[j][u];
                }
            }
        }
        if (vertex) ans = join(ans, {value[c], value[c], value[c]});
        return ans;
    }
    ll prefixSum(int a, int b) const {
        int c = lca(a, b);
        return pref[a] + pref[b] - 2 * pref[c] + (vertex ? value[c] : 0);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, root;
    char mode;
    cin >> n >> q >> root >> mode;
    vector<ll> val(n + 1);
    if (mode == 'V') for (int u = 1; u <= n; u++) cin >> val[u];
    PathJump g(n);
    for (int i = 1, a, b; i < n; i++) {
        ll w = 0;
        cin >> a >> b;
        if (mode == 'E') cin >> w;
        g.add(a, b, w);
    }
    g.build(root, val, mode == 'V');
    while (q--) {
        char type;
        int a, b;
        cin >> type >> a >> b;
        if (type == 'S') cout << g.prefixSum(a, b) << '\n';
        else {
            auto ans = g.path(a, b);
            cout << g.lca(a, b) << ' ';
            if (ans.mn == INF) cout << "EMPTY 0\n";
            else cout << ans.mn << ' ' << ans.mx << ' ' << ans.sum << '\n';
        }
    }
}

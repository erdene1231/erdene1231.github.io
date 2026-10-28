#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll INF = 1LL << 62;
int lg;
vector<int> dep;
vector<ll> pref;
vector<vector<int>> up;
vector<vector<ll>> mn, mx;

void build(const vector<vector<pair<int, ll>>>& adj) {
    int n = int(adj.size()) - 1;
    lg = 1;
    while ((1LL << lg) <= n) {
        ++lg;
    }
    dep.assign(n + 1, -1);
    pref.assign(n + 1, 0);
    up.assign(lg, vector<int>(n + 1, 1));
    mn.assign(lg, vector<ll>(n + 1, INF));
    mx.assign(lg, vector<ll>(n + 1, -INF));
    queue<int> q;
    dep[1] = 0;
    q.push(1);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (auto [v, w] : adj[u]) {
            if (dep[v] != -1) {
                continue;
            }
            dep[v] = dep[u] + 1;
            pref[v] = pref[u] + w;
            up[0][v] = u;
            mn[0][v] = mx[0][v] = w;
            q.push(v);
        }
    }
    for (int j = 1; j < lg; ++j) {
        for (int u = 1; u <= n; ++u) {
            int v = up[j - 1][u];
            up[j][u] = up[j - 1][v];
            mn[j][u] = min(mn[j - 1][u], mn[j - 1][v]);
            mx[j][u] = max(mx[j - 1][u], mx[j - 1][v]);
        }
    }
}

int lca(int u, int v) {
    if (dep[u] < dep[v]) {
        swap(u, v);
    }
    int d = dep[u] - dep[v];
    for (int j = 0; j < lg; ++j) {
        if ((d >> j) & 1) {
            u = up[j][u];
        }
    }
    if (u == v) {
        return u;
    }
    for (int j = lg - 1; j >= 0; --j) {
        if (up[j][u] != up[j][v]) {
            u = up[j][u];
            v = up[j][v];
        }
    }
    return up[0][u];
}

array<ll, 3> path_info(int a, int b, int c) {
    if (a == b) {
        return {0, 0, 0};
    }
    ll lo = INF, hi = -INF;
    for (int u : {a, b}) {
        int d = dep[u] - dep[c];
        for (int j = 0; j < lg; ++j) {
            if ((d >> j) & 1) {
                lo = min(lo, mn[j][u]);
                hi = max(hi, mx[j][u]);
                u = up[j][u];
            }
        }
    }
    return {lo, hi, pref[a] + pref[b] - 2 * pref[c]};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<vector<pair<int, ll>>> adj(n + 1);
    for (int i = 0; i < n - 1; ++i) {
        int u, v;
        ll w;
        cin >> u >> v >> w;
        adj[u].push_back({v, w});
        adj[v].push_back({u, w});
    }
    build(adj);
    while (q--) {
        int u, v;
        cin >> u >> v;
        int c = lca(u, v);
        auto [lo, hi, sum] = path_info(u, v, c);
        cout << c << ' ' << lo << ' ' << hi << ' ' << sum << '\n';
    }
}

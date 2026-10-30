#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll INF = 1LL << 60;

struct Edge {
    int a, b;
    ll w;
};

struct Bellman {
    int n;
    vector<Edge> e;
    vector<vector<int>> adj;
    vector<ll> d;
    vector<int> par, bad;

    Bellman(int _n) {
        n = _n;
        adj.resize(n + 1);
        d.assign(n + 1, INF);
        par.assign(n + 1, -1);
        bad.resize(n + 1);
    }

    void add(int a, int b, ll w) {
        e.push_back({a, b, w});
        adj[a].push_back(b);
    }

    void run(int s) {
        d[s] = 0;
        for (int i = 1; i < n; i++) {
            bool changed = false;
            for (auto [a, b, w] : e) {
                if (d[a] == INF) continue;
                ll nd = d[a] + w;
                if (nd < d[b]) {
                    d[b] = nd;
                    par[b] = a;
                    changed = true;
                }
            }
            if (!changed) break;
        }
        queue<int> q;
        for (auto [a, b, w] : e) {
            if (d[a] != INF && d[a] + w < d[b] && !bad[b]) {
                bad[b] = 1;
                q.push(b);
            }
        }
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : adj[v]) {
                if (!bad[u]) {
                    bad[u] = 1;
                    q.push(u);
                }
            }
        }
    }

    vector<int> path(int t) const {
        if (d[t] == INF || bad[t]) return {};
        vector<int> p;
        for (int v = t; v != -1; v = par[v]) p.push_back(v);
        reverse(p.begin(), p.end());
        return p;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, s, q;
    cin >> n >> m >> s >> q;
    Bellman bf(n);
    while (m--) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        bf.add(a, b, w);
    }
    bf.run(s);
    while (q--) {
        int t;
        cin >> t;
        if (bf.bad[t]) cout << "-INF\n";
        else if (bf.d[t] == INF) cout << "UNREACHABLE\n";
        else {
            auto p = bf.path(t);
            cout << bf.d[t] << ' ' << p.size();
            for (int v : p) cout << ' ' << v;
            cout << '\n';
        }
    }
    return 0;
}

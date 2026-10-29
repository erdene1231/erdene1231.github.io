#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Flow {
    struct Edge {
        int a, b;
        ll cap;
    };
    int n;
    ll mx = 0, timer = 0;
    vector<Edge> e;
    vector<vector<int>> adj;
    vector<int> par;
    vector<ll> seen;
    Flow(int _n) {
        n = _n;
        adj.resize(n);
        par.resize(n);
        seen.resize(n);
    }
    int add(int a, int b, ll c) {
        int id = (int)e.size();
        adj[a].push_back(id);
        e.push_back({a, b, c});
        adj[b].push_back(id + 1);
        e.push_back({b, a, 0});
        mx = max(mx, c);
        return id;
    }
    ll augment(int s, int t, ll lim, bool bfs) {
        timer++;
        deque<int> q = {s};
        seen[s] = timer;
        while (!q.empty() && seen[t] != timer) {
            int u = bfs ? q.front() : q.back();
            if (bfs) q.pop_front();
            else q.pop_back();
            for (int id : adj[u]) {
                int v = e[id].b;
                if (e[id].cap < lim || seen[v] == timer) continue;
                seen[v] = timer;
                par[v] = id;
                q.push_back(v);
            }
        }
        if (seen[t] != timer) return 0;
        ll x = 1LL << 62;
        for (int u = t; u != s; u = e[par[u]].a) x = min(x, e[par[u]].cap);
        for (int u = t; u != s; u = e[par[u]].a) {
            int id = par[u];
            e[id].cap -= x;
            e[id ^ 1].cap += x;
        }
        return x;
    }
    ll run(int s, int t, char mode = 'E') {
        ll lim = 1, ans = 0;
        if (mode == 'S') while (lim <= mx / 2) lim *= 2;
        do {
            while (true) {
                ll x = augment(s, t, lim, mode == 'E');
                if (!x) break;
                ans += x;
            }
            lim = mode == 'S' ? lim / 2 : 0;
        } while (lim);
        return ans;
    }
    vector<int> reachable(int s) const {
        vector<int> vis(n), q = {s};
        vis[s] = true;
        for (int i = 0; i < (int)q.size(); i++) {
            int u = q[i];
            for (int id : adj[u]) {
                int v = e[id].b;
                if (e[id].cap > 0 && !vis[v]) vis[v] = true, q.push_back(v);
            }
        }
        return vis;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int l, r, m;
    cin >> l >> r >> m;
    int s = l + r, t = s + 1;
    Flow g(t + 1);
    for (int u = 0; u < l; u++) g.add(s, u, 1);
    for (int v = 0; v < r; v++) g.add(l + v, t, 1);
    vector<array<int, 3>> edges;
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        --a; --b;
        int id = g.add(a, l + b, 1);
        edges.push_back({a, b, id});
    }
    cout << g.run(s, t) << '\n';
    for (auto [a, b, id] : edges) if (g.e[id ^ 1].cap) cout << a + 1 << ' ' << b + 1 << '\n';
    auto z = g.reachable(s);
    vector<int> cover, independent, x, neighbors;
    for (int u = 0; u < l; u++) {
        if (!z[u]) cover.push_back(u + 1);
        else independent.push_back(u + 1), x.push_back(u + 1);
    }
    for (int v = 0; v < r; v++) {
        if (z[l + v]) cover.push_back(l + v + 1), neighbors.push_back(v + 1);
        else independent.push_back(l + v + 1);
    }
    auto print = [](const string &name, const vector<int> &a) {
        cout << name << ' ' << a.size();
        for (int u : a) cout << ' ' << u;
        cout << '\n';
    };
    print("COVER", cover);
    print("INDEPENDENT", independent);
    if (x.size() > neighbors.size()) {
        print("HALL", x);
        print("NEIGHBORS", neighbors);
    } else cout << "LEFT SATURATED\n";
}

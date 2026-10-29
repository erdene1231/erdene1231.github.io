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

vector<int> takePath(Flow &g, int s, int t) {
    vector<int> par(g.n, -1), q = {s};
    par[s] = -2;
    for (int i = 0; i < (int)q.size() && par[t] == -1; i++) {
        int u = q[i];
        for (int id : g.adj[u]) {
            int v = g.e[id].b;
            if ((id & 1) || g.e[id ^ 1].cap == 0 || par[v] != -1) continue;
            par[v] = id;
            q.push_back(v);
        }
    }
    if (par[t] == -1) return {};
    vector<int> path;
    for (int u = t; u != s; u = g.e[par[u]].a) {
        path.push_back(u);
        int id = par[u];
        g.e[id ^ 1].cap--;
        g.e[id].cap++;
    }
    path.push_back(s);
    reverse(path.begin(), path.end());
    return path;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, s, t;
    char mode;
    cin >> n >> m >> s >> t >> mode;
    --s; --t;
    bool vertex = mode == 'V';
    Flow g(vertex ? 2 * n : n);
    if (vertex) for (int u = 0; u < n; u++) g.add(2 * u, 2 * u + 1, u == s || u == t ? m + 1 : 1);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        --a; --b;
        g.add(vertex ? 2 * a + 1 : a, vertex ? 2 * b : b, 1);
    }
    int source = vertex ? 2 * s : s, sink = vertex ? 2 * t + 1 : t;
    ll count = g.run(source, sink);
    cout << count << '\n';
    for (ll i = 0; i < count; i++) {
        auto path = takePath(g, source, sink);
        vector<int> ans;
        for (int u : path) {
            int v = vertex ? u / 2 : u;
            if (ans.empty() || ans.back() != v) ans.push_back(v);
        }
        cout << ans.size();
        for (int u : ans) cout << ' ' << u + 1;
        cout << '\n';
    }
}

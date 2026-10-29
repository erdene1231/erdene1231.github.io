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
    int n, m, s, t;
    char mode;
    cin >> n >> m >> s >> t >> mode;
    --s; --t;
    Flow g(n);
    vector<int> ids;
    vector<ll> cap;
    for (int i = 0, a, b; i < m; i++) {
        ll c;
        cin >> a >> b >> c;
        ids.push_back(g.add(a - 1, b - 1, c));
        cap.push_back(c);
    }
    ll value = g.run(s, t, mode);
    auto vis = g.reachable(s);
    ll cut = 0;
    for (int i = 0; i < m; i++) {
        auto edge = g.e[ids[i]];
        if (vis[edge.a] && !vis[edge.b]) cut += cap[i];
    }
    cout << value << ' ' << cut << '\n';
    for (int u = 0; u < n; u++) cout << vis[u] << ' ';
    cout << '\n';
    for (int id : ids) cout << g.e[id ^ 1].cap << ' ';
    cout << '\n';
}

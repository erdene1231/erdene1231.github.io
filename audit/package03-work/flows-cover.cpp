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
    int n, m;
    char mode;
    cin >> n >> m >> mode;
    vector<vector<int>> adj(n);
    vector<vector<int>> allowed(n, vector<int>(n)), first(n, vector<int>(n, -1));
    vector<int> deg(n), ord;
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        adj[--a].push_back(--b);
        allowed[a][b] = true;
        deg[b]++;
    }
    for (int u = 0; u < n; u++) if (!deg[u]) ord.push_back(u);
    for (int i = 0; i < (int)ord.size(); i++) {
        for (int v : adj[ord[i]]) if (--deg[v] == 0) ord.push_back(v);
    }
    if ((int)ord.size() != n) {
        cout << "NOT A DAG\n";
        return 0;
    }
    if (mode == 'G') {
        for (int s = 0; s < n; s++) {
            vector<int> q = {s};
            first[s][s] = s;
            for (int i = 0; i < (int)q.size(); i++) {
                int u = q[i];
                for (int v : adj[u]) {
                    if (first[s][v] != -1) continue;
                    first[s][v] = u == s ? v : first[s][u];
                    q.push_back(v);
                }
            }
            for (int v = 0; v < n; v++) allowed[s][v] = v != s && first[s][v] != -1;
        }
    }
    int s = 2 * n, t = s + 1;
    Flow g(t + 1);
    for (int u = 0; u < n; u++) g.add(s, u, 1), g.add(n + u, t, 1);
    vector<array<int, 3>> edges;
    for (int u = 0; u < n; u++) for (int v = 0; v < n; v++) {
        if (allowed[u][v]) edges.push_back({u, v, g.add(u, n + v, 1)});
    }
    ll count = n - g.run(s, t);
    vector<int> to(n, -1), prev(n, -1);
    for (auto [u, v, id] : edges) if (g.e[id ^ 1].cap) to[u] = v, prev[v] = u;
    cout << count << '\n';
    for (int start = 0; start < n; start++) {
        if (prev[start] != -1) continue;
        vector<int> path = {start};
        for (int u = start; to[u] != -1; u = to[u]) {
            int v = to[u];
            if (mode == 'G') {
                int x = u;
                while (x != v) x = first[x][v], path.push_back(x);
            } else path.push_back(v);
        }
        cout << path.size();
        for (int u : path) cout << ' ' << u + 1;
        cout << '\n';
    }
    if (mode == 'G') {
        auto z = g.reachable(s);
        vector<int> antichain;
        for (int u = 0; u < n; u++) if (z[u] && !z[n + u]) antichain.push_back(u + 1);
        cout << "ANTICHAIN " << antichain.size();
        for (int u : antichain) cout << ' ' << u;
        cout << '\n';
    }
}

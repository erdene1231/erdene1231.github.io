#include <bits/stdc++.h>
using namespace std;

struct Hamilton {
    int n;
    bool closed;
    vector<vector<int>> adj;
    vector<int> used, path;
    Hamilton(int _n) {
        n = _n;
        adj.assign(n, vector<int>(n));
        used.resize(n);
    }
    bool dfs(int u) {
        if ((int)path.size() == n) return !closed || adj[u][path[0]];
        for (int v = 0; v < n; v++) {
            if (!adj[u][v] || used[v]) continue;
            used[v] = true;
            path.push_back(v);
            if (dfs(v)) return true;
            path.pop_back();
            used[v] = false;
        }
        return false;
    }
    vector<int> solve(bool cycle) {
        closed = cycle;
        if (closed && n < 3) return {};
        for (int s = 0; s < (closed ? 1 : n); s++) {
            fill(used.begin(), used.end(), false);
            path = {s};
            used[s] = true;
            if (dfs(s)) {
                if (closed) path.push_back(s);
                return path;
            }
        }
        return {};
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, directed, closed;
    cin >> n >> m >> directed >> closed;
    Hamilton g(n);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.adj[--a][--b] = true;
        if (!directed) g.adj[b][a] = true;
    }
    auto ans = g.solve(closed);
    if (ans.empty()) cout << "IMPOSSIBLE\n";
    else {
        for (int u : ans) cout << u + 1 << ' ';
        cout << '\n';
    }
}

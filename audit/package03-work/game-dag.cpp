#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Game {
    int n;
    vector<vector<int>> adj;
    vector<int> g;
    Game(int _n) : n(_n), adj(n), g(n) {}
    bool build() {
        vector<int> deg(n), order;
        for (int u = 0; u < n; u++) for (int v : adj[u]) deg[v]++;
        queue<int> q;
        for (int u = 0; u < n; u++) if (deg[u] == 0) q.push(u);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            order.push_back(u);
            for (int v : adj[u]) if (--deg[v] == 0) q.push(v);
        }
        if ((int)order.size() != n) return false;
        reverse(order.begin(), order.end());
        for (int u : order) {
            int d = (int)adj[u].size();
            vector<bool> seen(d + 1);
            for (int v : adj[u]) if (g[v] <= d) seen[g[v]] = true;
            while (g[u] <= d && seen[g[u]]) g[u]++;
        }
        return true;
    }
};

int main() {
    int n, m, k;
    cin >> n >> m >> k;
    Game game(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        game.adj[u - 1].push_back(v - 1);
    }
    vector<int> pos(k);
    for (int &u : pos) {
        cin >> u;
        u--;
    }
    if (!game.build()) {
        cout << "INVALID: cycle\n";
        return 0;
    }
    int s = 0;
    for (int u : pos) s ^= game.g[u];
    for (int x : game.g) cout << x << ' ';
    cout << '\n';
    if (s == 0) cout << "LOSE\n";
    else {
        for (int i = 0; i < k; i++) {
            int u = pos[i], target = game.g[u] ^ s;
            if (target >= game.g[u]) continue;
            for (int v : game.adj[u]) {
                if (game.g[v] == target) {
                    cout << "WIN " << i + 1 << ' ' << v + 1 << '\n';
                    return 0;
                }
            }
        }
    }
}

#include <bits/stdc++.h>
using namespace std;

struct Bipartite {
    int n;
    vector<vector<int>> adj;
    vector<int> col;

    Bipartite(int _n) {
        n = _n;
        adj.resize(n + 1);
        col.assign(n + 1, -1);
    }

    bool fill(int s) {
        queue<int> q;
        col[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : adj[v]) {
                if (col[u] == -1) {
                    col[u] = col[v] ^ 1;
                    q.push(u);
                } else if (col[u] == col[v]) {
                    return false;
                }
            }
        }
        return true;
    }

    bool run() {
        for (int v = 1; v <= n; v++) {
            if (col[v] == -1 && !fill(v)) return false;
        }
        return true;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    Bipartite bp(n);
    while (m--) {
        int a, b;
        cin >> a >> b;
        bp.adj[a].push_back(b);
        bp.adj[b].push_back(a);
    }
    if (!bp.run()) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    for (int v = 1; v <= n; v++) cout << bp.col[v] + 1 << ' ';
    cout << '\n';
    return 0;
}

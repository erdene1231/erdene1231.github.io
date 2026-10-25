#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        cin >> u >> v;
        u--;
        v--;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> color(n, -1);
    for (int start = 0; start < n; start++) {
        if (color[start] != -1) {
            continue;
        }

        color[start] = 0;
        queue<int> q;
        q.push(start);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : adj[v]) {
                if (color[u] == -1) {
                    color[u] = 1 - color[v];
                    q.push(u);
                } else if (color[u] == color[v]) {
                    cout << "IMPOSSIBLE\n";
                    return 0;
                }
            }
        }
    }

    for (int i = 0; i < n; i++) {
        cout << color[i] + 1 << (i + 1 == n ? '\n' : ' ');
    }
    return 0;
}

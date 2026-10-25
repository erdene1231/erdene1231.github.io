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

    vector<int> component(n, 0);
    int count = 0;
    for (int start = 0; start < n; start++) {
        if (component[start] != 0) {
            continue;
        }

        count++;
        component[start] = count;
        queue<int> q;
        q.push(start);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : adj[v]) {
                if (component[u] == 0) {
                    component[u] = count;
                    q.push(u);
                }
            }
        }
    }

    cout << count << '\n';
    for (int i = 0; i < n; i++) {
        cout << component[i] << (i + 1 == n ? '\n' : ' ');
    }
    return 0;
}

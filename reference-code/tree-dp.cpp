#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<int>> adj(n);
    for (int i = 0; i < n - 1; i++) {
        int u, v;
        cin >> u >> v;
        u--;
        v--;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    vector<int> parent(n, -1);
    vector<int> order = {0};
    for (int i = 0; i < n; i++) {
        int v = order[i];
        for (int u : adj[v]) {
            if (u != parent[v]) {
                parent[u] = v;
                order.push_back(u);
            }
        }
    }

    const long long MOD = 1000000007;
    vector<long long> white(n, 1), black(n, 1);
    for (int i = n - 1; i >= 0; i--) {
        int v = order[i];
        for (int u : adj[v]) {
            if (u == parent[v]) {
                continue;
            }
            white[v] = white[v] * ((white[u] + black[u]) % MOD) % MOD;
            black[v] = black[v] * white[u] % MOD;
        }
    }

    cout << (white[0] + black[0]) % MOD << '\n';
    return 0;
}

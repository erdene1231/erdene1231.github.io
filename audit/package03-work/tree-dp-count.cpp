#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll MOD = 1000000007;

struct TreeDP {
    int n;
    vector<vector<int>> adj;
    vector<int> par, ord;
    vector<array<ll, 2>> dp;
    TreeDP(int _n) {
        n = _n;
        adj.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    ll run(int r) {
        par.assign(n + 1, 0);
        ord = {r};
        for (int i = 0; i < (int)ord.size(); i++) {
            int u = ord[i];
            for (int v : adj[u]) {
                if (v == par[u]) continue;
                par[v] = u;
                ord.push_back(v);
            }
        }
        dp.assign(n + 1, {1, 1});
        for (int i = n - 1; i >= 0; i--) {
            int u = ord[i];
            for (int v : adj[u]) {
                if (v == par[u]) continue;
                dp[u][0] = dp[u][0] * ((dp[v][0] + dp[v][1]) % MOD) % MOD;
                dp[u][1] = dp[u][1] * dp[v][0] % MOD;
            }
        }
        return (dp[r][0] + dp[r][1]) % MOD;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    TreeDP g(n);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    cout << g.run(1) << '\n';
}

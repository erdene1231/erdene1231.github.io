#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<string> g(n);
    for (string &row : g) cin >> row;
    const ll MOD = 1000000007;
    vector<ll> dp(m);
    dp[0] = 1;

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (g[i][j] == '*') dp[j] = 0;
            else if (j > 0) dp[j] = (dp[j] + dp[j - 1]) % MOD;
        }
    }
    cout << dp[m - 1] << '\n';
}

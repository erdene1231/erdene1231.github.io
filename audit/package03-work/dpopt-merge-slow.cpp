#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<ll> s(n + 1);
    for (int i = 1, x; i <= n; i++) {
        cin >> x;
        s[i] = s[i - 1] + x;
    }
    vector<vector<ll>> dp(n + 1, vector<ll>(n + 1));
    const ll INF = 1LL << 62;
    for (int len = 2; len <= n; len++) {
        for (int l = 1; l + len - 1 <= n; l++) {
            int r = l + len - 1;
            dp[l][r] = INF;
            for (int j = l; j < r; j++) {
                ll val = dp[l][j] + dp[j + 1][r] + s[r] - s[l - 1];
                dp[l][r] = min(dp[l][r], val);
            }
        }
    }
    cout << dp[1][n] << '\n';
}

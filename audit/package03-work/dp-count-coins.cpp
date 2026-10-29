#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000000007;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k, n;
    if (!(cin >> k >> n)) return 0;
    vector<int> c(k), dp(n + 1);
    for (int& x : c) cin >> x;
    dp[0] = 1;
    for (int x = 1; x <= n; x++) {
        for (int coin : c) {
            if (x < coin) continue;
            dp[x] += dp[x - coin];
            if (dp[x] >= MOD) dp[x] -= MOD;
        }
    }
    cout << dp[n] << '\n';
}

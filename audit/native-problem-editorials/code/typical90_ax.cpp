#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, l;
    cin >> n >> l;
    const int mod = 1000000007;
    vector<int> dp(n + 1);
    dp[0] = 1;
    for (int i = 1; i <= n; ++i) {
        dp[i] = dp[i - 1];
        if (i >= l) {
            dp[i] += dp[i - l];
            if (dp[i] >= mod) dp[i] -= mod;
        }
    }
    cout << dp[n] << '\n';
}

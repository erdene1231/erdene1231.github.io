#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k;
    cin >> k;
    if (k % 9 != 0) {
        cout << 0 << '\n';
        return 0;
    }
    const int mod = 1000000007;
    vector<int> dp(k + 1);
    dp[0] = 1;
    for (int sum = 1; sum <= k; ++sum) {
        ll ways = 0;
        for (int d = 1; d <= 9 && d <= sum; ++d) ways += dp[sum - d];
        dp[sum] = int(ways % mod);
    }
    cout << dp[k] << '\n';
}

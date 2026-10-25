#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<long long> prefix(n + 1, 0);
    for (int i = 0; i < n; i++) {
        long long x;
        cin >> x;
        prefix[i + 1] = prefix[i] + x;
    }

    const long long INF = LLONG_MAX / 4;
    vector<vector<long long>> dp(n, vector<long long>(n, 0));

    for (int length = 2; length <= n; length++) {
        for (int l = 0; l + length <= n; l++) {
            int r = l + length - 1;
            long long sum = prefix[r + 1] - prefix[l];
            dp[l][r] = INF;

            for (int k = l; k < r; k++) {
                long long cost = dp[l][k] + dp[k + 1][r] + sum;
                dp[l][r] = min(dp[l][r], cost);
            }
        }
    }

    cout << dp[0][n - 1] << '\n';
    return 0;
}

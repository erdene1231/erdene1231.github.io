#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<long double> dice(int n) {
    vector<long double> dp(6 * n + 1);
    dp[0] = 1;
    for (int i = 0; i < n; i++) {
        vector<long double> ndp(6 * n + 1);
        for (int s = 0; s <= 6 * i; s++) {
            for (int x = 1; x <= 6; x++) {
                ndp[s + x] += dp[s] / 6;
            }
        }
        dp.swap(ndp);
    }
    return dp;
}

int main() {
    int n, l, r;
    cin >> n >> l >> r;
    auto dp = dice(n);
    long double ans = 0, mean = 0;
    for (int s = 0; s <= 6 * n; s++) {
        if (l <= s && s <= r) ans += dp[s];
        mean += s * dp[s];
    }
    cout << fixed << setprecision(18) << ans << ' ' << mean << '\n';
    for (auto p : dp) cout << p << ' ';
    cout << '\n';
}

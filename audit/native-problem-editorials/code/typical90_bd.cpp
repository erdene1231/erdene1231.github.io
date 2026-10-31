#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, s;
    cin >> n >> s;
    vector<int> a(n), b(n);
    for (int i = 0; i < n; ++i) cin >> a[i] >> b[i];
    vector<vector<char>> dp(n + 1, vector<char>(s + 1));
    dp[0][0] = true;
    for (int i = 0; i < n; ++i) {
        for (int sum = 0; sum <= s; ++sum) {
            if (!dp[i][sum]) continue;
            if (sum + a[i] <= s) dp[i + 1][sum + a[i]] = true;
            if (sum + b[i] <= s) dp[i + 1][sum + b[i]] = true;
        }
    }
    if (!dp[n][s]) {
        cout << "Impossible\n";
        return 0;
    }
    string ans(n, 'A');
    int rem = s;
    for (int i = n - 1; i >= 0; --i) {
        if (rem >= a[i] && dp[i][rem - a[i]]) rem -= a[i];
        else {
            ans[i] = 'B';
            rem -= b[i];
        }
    }
    cout << ans << '\n';
}

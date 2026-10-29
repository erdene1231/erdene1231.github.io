#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<vector<int>> a(n + 1, vector<int>(n + 1));
    vector<vector<ll>> dp(n + 1, vector<ll>(n + 1));
    for (int r = 1; r <= n; r++) {
        for (int c = 1; c <= n; c++) {
            cin >> a[r][c];
            dp[r][c] = max(dp[r - 1][c], dp[r][c - 1]) + a[r][c];
        }
    }
    cout << dp[n][n] << '\n';
    vector<pair<int, int>> path;
    int r = n, c = n;
    while (true) {
        path.push_back({r, c});
        if (r == 1 && c == 1) break;
        if (r > 1 && (c == 1 || dp[r - 1][c] >= dp[r][c - 1])) r--;
        else c--;
    }
    reverse(path.begin(), path.end());
    for (auto [y, x] : path) cout << y << ' ' << x << '\n';
}

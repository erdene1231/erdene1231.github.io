#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    vector<int> w(n);
    vector<ll> v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
    vector<vector<ll>> dp(n + 1, vector<ll>(W + 1));
    for (int k = 1; k <= n; k++) {
        for (int c = 0; c <= W; c++) {
            dp[k][c] = dp[k - 1][c];
            if (c >= w[k - 1]) {
                dp[k][c] = max(dp[k][c], dp[k - 1][c - w[k - 1]] + v[k - 1]);
            }
        }
    }
    vector<int> take;
    int c = W;
    for (int k = n; k >= 1; k--) {
        if (dp[k][c] != dp[k - 1][c]) {
            take.push_back(k);
            c -= w[k - 1];
        }
    }
    reverse(take.begin(), take.end());
    cout << dp[n][W] << '\n' << take.size() << '\n';
    for (int id : take) cout << id << ' ';
    cout << '\n';
}

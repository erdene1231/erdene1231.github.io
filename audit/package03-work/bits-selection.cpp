#include <bits/stdc++.h>
using namespace std;

using ll = long long;

ll selection(const vector<vector<int>>& price, int n) {
    int k = price.size(), states = 1 << k;
    const ll INF = 4'000'000'000'000'000'000LL;
    vector<vector<ll>> dp(n + 1, vector<ll>(states, INF));
    dp[0][0] = 0;
    for (int d = 0; d < n; d++) {
        dp[d + 1] = dp[d];
        for (int s = 0; s < states; s++) {
            for (int x = 0; x < k; x++) {
                if ((s & (1 << x)) && dp[d][s ^ (1 << x)] != INF) {
                    dp[d + 1][s] = min(dp[d + 1][s], dp[d][s ^ (1 << x)] + price[x][d]);
                }
            }
        }
    }
    return dp[n][states - 1] == INF ? -1 : dp[n][states - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k, n;
    cin >> k >> n;
    vector<vector<int>> price(k, vector<int>(n));
    for (auto& row : price) for (int& x : row) cin >> x;
    cout << selection(price, n) << '\n';
}

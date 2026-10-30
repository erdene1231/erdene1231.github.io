#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll INF = 1LL << 60;

ll minCost(const vector<vector<ll>> &price, int k, int n) {
    int m = 1 << k;
    vector<ll> dp(m, INF);
    dp[0] = 0;
    for (int d = 0; d < n; d++) {
        vector<ll> ndp = dp;
        for (int s = 0; s < m; s++) {
            if (dp[s] == INF) continue;
            for (int j = 0; j < k; j++) {
                if (!(s & (1 << j))) {
                    int t = s | (1 << j);
                    ndp[t] = min(ndp[t], dp[s] + price[j][d]);
                }
            }
        }
        dp.swap(ndp);
    }
    return dp[m - 1] == INF ? -1 : dp[m - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k, n;
    cin >> k >> n;
    vector<vector<ll>> price(k, vector<ll>(n));
    for (auto &row : price) {
        for (ll &x : row) cin >> x;
    }
    cout << minCost(price, k, n) << '\n';
    return 0;
}

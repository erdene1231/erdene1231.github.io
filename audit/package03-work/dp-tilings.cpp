#include <bits/stdc++.h>
using namespace std;

const int MOD = 1000000007;
int m;
vector<int> next_dp;

void fill_row(int col, int mask, int next_mask, int ways) {
    if (col == m) {
        next_dp[next_mask] += ways;
        if (next_dp[next_mask] >= MOD) next_dp[next_mask] -= MOD;
        return;
    }
    if (mask & (1 << col)) {
        fill_row(col + 1, mask, next_mask, ways);
        return;
    }
    if (col + 1 < m && !(mask & (1 << (col + 1)))) {
        fill_row(col + 2, mask, next_mask, ways);
    }
    fill_row(col + 1, mask, next_mask | (1 << col), ways);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n >> m)) return 0;
    if (n < m) swap(n, m);
    vector<int> dp(1 << m);
    dp[0] = 1;
    for (int row = 0; row < n; row++) {
        next_dp.assign(1 << m, 0);
        for (int mask = 0; mask < (1 << m); mask++) {
            if (dp[mask]) fill_row(0, mask, 0, dp[mask]);
        }
        dp.swap(next_dp);
    }
    cout << dp[0] << '\n';
}

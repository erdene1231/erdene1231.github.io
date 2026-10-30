#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MOD = 1000000007;

int countMatching(const vector<vector<int>> &a) {
    int n = a.size();
    int m = 1 << n;
    vector<int> dp(m);
    dp[0] = 1;
    for (int s = 0; s < m; s++) {
        int i = __builtin_popcount((unsigned)s);
        if (i == n) continue;
        for (int j = 0; j < n; j++) {
            if (!(s & (1 << j)) && a[i][j]) {
                int t = s | (1 << j);
                dp[t] += dp[s];
                if (dp[t] >= MOD) dp[t] -= MOD;
            }
        }
    }
    return dp[m - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<vector<int>> a(n, vector<int>(n));
    for (auto &row : a) {
        for (int &x : row) cin >> x;
    }
    cout << countMatching(a) << '\n';
    return 0;
}

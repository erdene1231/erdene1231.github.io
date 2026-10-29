#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> w(n);
    int W = 0;
    for (int &x : w) {
        cin >> x;
        W += x;
    }
    vector<vector<char>> dp(n + 1, vector<char>(W + 1));
    dp[0][0] = true;
    for (int k = 1; k <= n; k++) {
        for (int x = 0; x <= W; x++) {
            dp[k][x] = dp[k - 1][x];
            if (x >= w[k - 1]) dp[k][x] |= dp[k - 1][x - w[k - 1]];
        }
    }
    for (int x = 0; x <= W; x++) cout << int(dp[n][x]) << (x == W ? '\n' : ' ');
}

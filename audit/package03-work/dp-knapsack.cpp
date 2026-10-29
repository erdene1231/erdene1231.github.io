#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> w(n);
    int sum = 0;
    for (int& x : w) {
        cin >> x;
        sum += x;
    }
    vector<vector<char>> dp(n + 1, vector<char>(sum + 1));
    dp[0][0] = true;
    for (int k = 1; k <= n; k++) {
        for (int x = 0; x <= sum; x++) {
            dp[k][x] = dp[k - 1][x];
            if (x >= w[k - 1]) dp[k][x] |= dp[k - 1][x - w[k - 1]];
        }
    }
    vector<char> possible(sum + 1);
    possible[0] = true;
    for (int weight : w) {
        for (int x = sum; x >= weight; x--) {
            possible[x] |= possible[x - weight];
        }
    }
    for (int x = 0; x <= sum; x++) if (dp[n][x]) cout << x << ' ';
    cout << '\n';
    for (int x = 0; x <= sum; x++) if (possible[x]) cout << x << ' ';
    cout << '\n';
}

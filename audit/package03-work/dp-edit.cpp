#include <bits/stdc++.h>
using namespace std;

struct Op {
    char type, from, to;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string x, y;
    if (!getline(cin, x) || !getline(cin, y)) return 0;
    int n = x.size(), m = y.size();
    vector<vector<int>> dp(n + 1, vector<int>(m + 1));
    for (int i = 0; i <= n; i++) dp[i][0] = i;
    for (int j = 0; j <= m; j++) dp[0][j] = j;
    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= m; j++) {
            int cost = (x[i - 1] != y[j - 1]);
            dp[i][j] = min({dp[i - 1][j] + 1, dp[i][j - 1] + 1,
                            dp[i - 1][j - 1] + cost});
        }
    }
    vector<Op> ans;
    int i = n, j = m;
    while (i > 0 || j > 0) {
        if (i > 0 && j > 0 && x[i - 1] == y[j - 1]) {
            ans.push_back({'K', x[i - 1], y[j - 1]});
            i--; j--;
        } else if (i > 0 && j > 0 && dp[i][j] == dp[i - 1][j - 1] + 1) {
            ans.push_back({'R', x[i - 1], y[j - 1]});
            i--; j--;
        } else if (i > 0 && dp[i][j] == dp[i - 1][j] + 1) {
            ans.push_back({'D', x[i - 1], '-'});
            i--;
        } else {
            ans.push_back({'I', '-', y[j - 1]});
            j--;
        }
    }
    reverse(ans.begin(), ans.end());
    cout << dp[n][m] << '\n';
    for (auto op : ans) cout << op.type << ' ' << op.from << ' ' << op.to << '\n';
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<vector<ll>> a(n, vector<ll>(m));
    for (auto &row : a) {
        for (ll &x : row) cin >> x;
    }
    vector<string> g(n);
    for (string &row : g) cin >> row;

    const ll NEG = -(1LL << 60);
    vector<vector<ll>> dp(n, vector<ll>(m, NEG));
    vector<vector<char>> par(n, vector<char>(m));
    if (g[0][0] == '.') dp[0][0] = a[0][0];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (g[i][j] == '*' || (i == 0 && j == 0)) continue;
            ll best = NEG;
            if (i > 0 && dp[i - 1][j] != NEG) {
                best = dp[i - 1][j];
                par[i][j] = 'D';
            }
            if (j > 0 && dp[i][j - 1] > best) {
                best = dp[i][j - 1];
                par[i][j] = 'R';
            }
            if (best != NEG) dp[i][j] = best + a[i][j];
        }
    }

    if (dp[n - 1][m - 1] == NEG) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    string path;
    int i = n - 1, j = m - 1;
    while (i != 0 || j != 0) {
        char c = par[i][j];
        path += c;
        if (c == 'D') i--;
        else j--;
    }
    reverse(path.begin(), path.end());
    cout << dp[n - 1][m - 1] << '\n' << path << '\n';
}

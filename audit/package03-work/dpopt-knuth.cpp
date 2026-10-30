#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Knuth {
    static constexpr ll INF = 1LL << 62;
    int n;
    vector<ll> s;
    vector<vector<ll>> dp;
    vector<vector<int>> opt;
    Knuth(int _n) {
        n = _n;
        s.resize(n + 1);
        dp.assign(n + 1, vector<ll>(n + 1));
        opt.assign(n + 1, vector<int>(n + 1));
        for (int i = 1; i <= n; i++) opt[i][i] = i;
    }
    ll run() {
        for (int len = 2; len <= n; len++) {
            for (int l = 1; l + len - 1 <= n; l++) {
                int r = l + len - 1;
                int ql = opt[l][r - 1];
                int qr = min(r - 1, opt[l + 1][r]);
                dp[l][r] = INF;
                for (int j = ql; j <= qr; j++) {
                    ll val = dp[l][j] + dp[j + 1][r] + s[r] - s[l - 1];
                    if (val <= dp[l][r]) {
                        dp[l][r] = val;
                        opt[l][r] = j;
                    }
                }
            }
        }
        return dp[1][n];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    Knuth dp(n);
    for (int i = 1, x; i <= n; i++) {
        cin >> x;
        dp.s[i] = dp.s[i - 1] + x;
    }
    cout << dp.run() << '\n';
}

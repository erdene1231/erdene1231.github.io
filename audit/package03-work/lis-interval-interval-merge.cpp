#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct MergeDP {
    int n;
    vector<ll> pref;
    vector<vector<ll>> dp;
    vector<vector<int>> cut;

    MergeDP(const vector<ll> &a) {
        n = a.size();
        pref.resize(n + 1);
        dp.assign(n, vector<ll>(n));
        cut.assign(n, vector<int>(n, -1));
        for (int i = 0; i < n; i++) pref[i + 1] = pref[i] + a[i];
    }

    ll solve() {
        for (int len = 2; len <= n; len++) {
            for (int l = 0; l + len <= n; l++) {
                int r = l + len - 1;
                dp[l][r] = 1LL << 60;
                ll sum = pref[r + 1] - pref[l];
                for (int k = l; k < r; k++) {
                    ll val = dp[l][k] + dp[k + 1][r] + sum;
                    if (val < dp[l][r]) {
                        dp[l][r] = val;
                        cut[l][r] = k;
                    }
                }
            }
        }
        return n == 0 ? 0 : dp[0][n - 1];
    }

    void print(int l, int r) {
        if (l == r) return;
        int k = cut[l][r];
        print(l, k);
        print(k + 1, r);
        cout << l + 1 << ' ' << k + 1 << ' ' << r + 1 << '\n';
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    MergeDP dp(a);
    cout << dp.solve() << '\n';
    if (n > 0) dp.print(0, n - 1);
}

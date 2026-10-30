#include <bits/stdc++.h>
using namespace std;
using ll = long long;

void subsetSums(vector<ll> &dp, int n) {
    for (int i = 0; i < n; i++) {
        for (int s = 0; s < (1 << n); s++) {
            if (s & (1 << i)) dp[s] += dp[s ^ (1 << i)];
        }
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    int m = 1 << n;
    vector<ll> dp(m);
    for (ll &x : dp) cin >> x;
    subsetSums(dp, n);
    for (int s = 0; s < m; s++) {
        if (s) cout << ' ';
        cout << dp[s];
    }
    cout << '\n';
    return 0;
}

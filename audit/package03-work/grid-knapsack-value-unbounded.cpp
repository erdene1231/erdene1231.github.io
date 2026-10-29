#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, W;
    cin >> n >> W;
    vector<int> w(n);
    vector<ll> v(n);
    for (int i = 0; i < n; i++) cin >> w[i] >> v[i];
    vector<ll> dp(W + 1);
    for (int k = 0; k < n; k++) {
        for (int c = w[k]; c <= W; c++) {
            dp[c] = max(dp[c], dp[c - w[k]] + v[k]);
        }
    }
    cout << dp[W] << '\n';
}

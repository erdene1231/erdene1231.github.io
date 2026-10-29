#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    vector<int> dp(n, 1), par(n, -1);
    int best = -1;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] < a[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                par[i] = j;
            }
        }
        if (best == -1 || dp[i] > dp[best]) best = i;
    }
    vector<int> path;
    for (int i = best; i != -1; i = par[i]) path.push_back(i);
    reverse(path.begin(), path.end());
    cout << path.size() << '\n';
    for (int i : path) cout << i + 1 << ' ';
    cout << '\n';
}

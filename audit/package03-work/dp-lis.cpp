#include <bits/stdc++.h>
using namespace std;

vector<int> lis(const vector<int>& a) {
    int n = a.size(), best = -1;
    vector<int> dp(n, 1), par(n, -1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] < a[i] && dp[j] + 1 > dp[i]) {
                dp[i] = dp[j] + 1;
                par[i] = j;
            }
        }
        if (best == -1 || dp[i] > dp[best]) best = i;
    }
    vector<int> ans;
    for (int i = best; i != -1; i = par[i]) ans.push_back(a[i]);
    reverse(ans.begin(), ans.end());
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    vector<int> ans = lis(a);
    cout << ans.size() << '\n';
    for (int x : ans) cout << x << ' ';
    cout << '\n';
}

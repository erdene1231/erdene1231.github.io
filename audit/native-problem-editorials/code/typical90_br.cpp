#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<ll> x(n), y(n);
    for (int i = 0; i < n; ++i) cin >> x[i] >> y[i];
    sort(x.begin(), x.end());
    sort(y.begin(), y.end());
    ll mx = x[n / 2], my = y[n / 2], ans = 0;
    for (int i = 0; i < n; ++i) ans += abs(x[i] - mx) + abs(y[i] - my);
    cout << ans << '\n';
}

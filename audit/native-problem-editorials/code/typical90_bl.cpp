#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1), d(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    ll ans = 0;
    for (int i = 1; i < n; ++i) {
        d[i] = a[i + 1] - a[i];
        ans += abs(d[i]);
    }
    auto change = [&](int i, ll delta) {
        ans -= abs(d[i]);
        d[i] += delta;
        ans += abs(d[i]);
    };
    while (q--) {
        int l, r;
        ll v;
        cin >> l >> r >> v;
        if (l > 1) change(l - 1, v);
        if (r < n) change(r, -v);
        cout << ans << '\n';
    }
}

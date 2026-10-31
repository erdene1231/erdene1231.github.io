#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<ll> u(n), v(n);
    for (int i = 0; i < n; ++i) {
        ll x, y;
        cin >> x >> y;
        u[i] = x + y;
        v[i] = x - y;
    }
    auto ub = minmax_element(u.begin(), u.end());
    auto vb = minmax_element(v.begin(), v.end());
    while (q--) {
        int k;
        cin >> k;
        --k;
        ll ans = max({u[k] - *ub.first, *ub.second - u[k],
            v[k] - *vb.first, *vb.second - v[k]});
        cout << ans << '\n';
    }
}

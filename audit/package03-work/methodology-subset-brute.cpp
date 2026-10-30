#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll count_brute(const vector<ll> &a, ll t) {
    int n = (int)a.size();
    assert(n <= 22);
    ll ans = 0;
    for (int mask = 0; mask < (1 << n); mask++) {
        ll s = 0;
        for (int i = 0; i < n; i++) {
            if (mask & (1 << i)) s += a[i];
        }
        if (s == t) ans++;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll t;
    cin >> n >> t;
    assert(0 <= n && n <= 22);
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    cout << count_brute(a, t) << '\n';
}

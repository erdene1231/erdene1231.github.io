#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll p, q;
    cin >> n >> p >> q;
    vector<ll> a(n);
    for (ll &x : a) {
        cin >> x;
        x %= p;
    }
    int ans = 0;
    for (int i = 0; i < n - 4; ++i) {
        for (int j = i + 1; j < n - 3; ++j) {
            ll p2 = a[i] * a[j] % p;
            for (int k = j + 1; k < n - 2; ++k) {
                ll p3 = p2 * a[k] % p;
                for (int l = k + 1; l < n - 1; ++l) {
                    ll p4 = p3 * a[l] % p;
                    for (int m = l + 1; m < n; ++m) {
                        if (p4 * a[m] % p == q) ++ans;
                    }
                }
            }
        }
    }
    cout << ans << '\n';
}

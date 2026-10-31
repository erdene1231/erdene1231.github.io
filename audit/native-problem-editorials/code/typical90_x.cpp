#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll k;
    cin >> n >> k;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    ll dist = 0;
    for (int i = 0; i < n; ++i) {
        ll b;
        cin >> b;
        dist += abs(a[i] - b);
    }
    bool ok = dist <= k && (k - dist) % 2 == 0;
    cout << (ok ? "Yes" : "No") << '\n';
}

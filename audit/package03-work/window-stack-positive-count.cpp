#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll x;
    cin >> n >> x;
    vector<ll> a(n);
    for (ll &v : a) cin >> v;
    int l = 0, ans = 0;
    ll sum = 0;
    for (int r = 0; r < n; r++) {
        sum += a[r];
        while (l <= r && sum > x) sum -= a[l++];
        if (l <= r && sum == x) ans++;
    }
    cout << ans << '\n';
}

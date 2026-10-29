#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    if (k < 1 || k > n) {
        cout << '\n';
        return 0;
    }
    ll sum = 0;
    for (int r = 0; r < n; r++) {
        sum += a[r];
        if (r >= k) sum -= a[r - k];
        if (r >= k - 1) cout << sum << (r == n - 1 ? '\n' : ' ');
    }
}

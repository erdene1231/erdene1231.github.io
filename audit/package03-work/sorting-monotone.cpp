#include <bits/stdc++.h>
using namespace std;
using ll = long long;

template<class F>
int first_true(int z, F ok) {
    int x = -1;
    for (int b = z; b >= 1; b /= 2) {
        while (x + b < z && !ok(x + b)) x += b;
    }
    return x + 1;
}

int peak_pos(const vector<ll>& f) {
    int n = f.size();
    if (n == 0) return -1;
    int x = -1;
    for (int b = n; b >= 1; b /= 2) {
        while (x + b < n - 1 && f[x + b] < f[x + b + 1]) x += b;
    }
    return x + 1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll t;
    int n;
    cin >> t >> n;
    vector<ll> f(n);
    for (ll& x : f) cin >> x;
    int ans = first_true(1000000000, [&](int x) {
        return 1LL * x * x >= t;
    });
    cout << ans << "\n";
    cout << peak_pos(f) << "\n";
    return 0;
}

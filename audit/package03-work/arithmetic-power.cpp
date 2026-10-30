#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll modpow(ll a, ll e, ll m) {
    a %= m;
    if (a < 0) a += m;
    ll r = 1 % m;
    while (e) {
        if (e & 1) r = r * a % m;
        a = a * a % m;
        e /= 2;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        ll a, e, m;
        cin >> a >> e >> m;
        cout << modpow(a, e, m) << '\n';
    }
}

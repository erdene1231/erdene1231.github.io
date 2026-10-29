#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool ropeOk(const vector<ll> &a, ll k, ll x) {
    ll need = k;
    for (ll v : a) {
        ll made = v / x;
        if (made >= need) return true;
        need -= made;
    }
    return false;
}

ll lastLength(const vector<ll> &a, ll k) {
    ll l = 0, r = 0;
    for (ll v : a) r = max(r, v);
    while (l < r) {
        ll gap = r - l;
        ll mid = l + gap / 2 + gap % 2;
        if (ropeOk(a, k, mid)) l = mid;
        else r = mid - 1;
    }
    return l;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll k;
    cin >> n >> k;
    vector<ll> a(n);
    for (ll &v : a) cin >> v;
    cout << lastLength(a, k) << '\n';
}

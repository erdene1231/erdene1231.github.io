#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int lowerBound(const vector<ll> &a, ll x) {
    int l = 0, r = a.size();
    while (l < r) {
        int mid = l + (r - l) / 2;
        if (a[mid] < x) l = mid + 1;
        else r = mid;
    }
    return l;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (ll &v : a) cin >> v;
    while (q--) {
        ll x;
        cin >> x;
        int p = lowerBound(a, x);
        cout << p << ' ' << p - 1 << '\n';
    }
}

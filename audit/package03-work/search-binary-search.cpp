#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int findAny(const vector<ll> &a, ll x) {
    int l = 0, r = (int)a.size() - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (a[mid] == x) return mid;
        if (a[mid] < x) l = mid + 1;
        else r = mid - 1;
    }
    return -1;
}

int findFirst(const vector<ll> &a, ll x) {
    int n = a.size(), k = -1, b = 1;
    while (b <= n / 2) b *= 2;
    for (; b >= 1; b /= 2) {
        while (k + b < n && a[k + b] < x) k += b;
    }
    int p = k + 1;
    return p < n && a[p] == x ? p : -1;
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
        cout << findAny(a, x) << ' ' << findFirst(a, x) << '\n';
    }
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Diff {
    int n;
    vector<ll> d;

    Diff(int _n) {
        n = _n;
        d.resize(n + 1);
    }

    void build(const vector<ll> &a) {
        fill(d.begin(), d.end(), 0);
        for (int i = 0; i < n; i++) {
            d[i] += a[i];
            d[i + 1] -= a[i];
        }
    }

    void add(int l, int r, ll x) {
        d[l] += x;
        d[r] -= x;
    }

    vector<ll> values() const {
        vector<ll> a(n);
        ll s = 0;
        for (int i = 0; i < n; i++) {
            s += d[i];
            a[i] = s;
        }
        return a;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    Diff diff(n);
    diff.build(a);
    while (q--) {
        int l, r;
        ll x;
        cin >> l >> r >> x;
        diff.add(l - 1, r, x);
    }
    a = diff.values();
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << a[i];
    }
    cout << '\n';
    return 0;
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Fenwick {
    int n;
    vector<ll> tree;
    Fenwick(int _n) {
        n = _n;
        tree.resize(n + 1);
    }
    void add(int k, ll x) {
        for (; k <= n; k += k & -k) tree[k] += x;
    }
    ll sum(int k) const {
        ll s = 0;
        for (; k > 0; k -= k & -k) s += tree[k];
        return s;
    }
    ll query(int l, int r) const {
        return sum(r) - sum(l - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    Fenwick diff(n);
    ll prev = 0;
    for (int i = 1; i <= n; i++) {
        ll x;
        cin >> x;
        diff.add(i, x - prev);
        prev = x;
    }
    while (q--) {
        int t;
        cin >> t;
        if (t == 1) {
            int l, r;
            ll x;
            cin >> l >> r >> x;
            diff.add(l, x);
            if (r < n) diff.add(r + 1, -x);
        } else {
            int k;
            cin >> k;
            cout << diff.sum(k) << '\n';
        }
    }
}

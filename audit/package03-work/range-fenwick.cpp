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
    Fenwick bit(n);
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        bit.add(i, x);
    }
    while (q--) {
        int t;
        cin >> t;
        if (t == 1) {
            int k;
            ll x;
            cin >> k >> x;
            bit.add(k, x);
        } else {
            int l, r;
            cin >> l >> r;
            cout << bit.query(l, r) << '\n';
        }
    }
}

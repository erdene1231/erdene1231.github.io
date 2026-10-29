#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Segtree {
    int n;
    vector<ll> tree;
    Segtree(int _n) {
        n = _n;
        tree.resize(n * 4 + 5);
    }
    void build(int v, int tl, int tr, const vector<int>& a) {
        if (tl == tr) {
            tree[v] = a[tl];
            return;
        }
        int tm = (tl + tr) / 2;
        build(v * 2, tl, tm, a);
        build(v * 2 + 1, tm + 1, tr, a);
        tree[v] = tree[v * 2] + tree[v * 2 + 1];
    }
    void add(int v, int tl, int tr, int k, ll x) {
        if (tl == tr) {
            tree[v] += x;
            return;
        }
        int tm = (tl + tr) / 2;
        if (k <= tm) add(v * 2, tl, tm, k, x);
        else add(v * 2 + 1, tm + 1, tr, k, x);
        tree[v] = tree[v * 2] + tree[v * 2 + 1];
    }
    ll query(int v, int tl, int tr, int l, int r) const {
        if (r < tl || tr < l) return 0;
        if (l <= tl && tr <= r) return tree[v];
        int tm = (tl + tr) / 2;
        return query(v * 2, tl, tm, l, r) + query(v * 2 + 1, tm + 1, tr, l, r);
    }
    void build(const vector<int>& a) { build(1, 0, n - 1, a); }
    void add(int k, ll x) { add(1, 0, n - 1, k, x); }
    ll query(int l, int r) const { return query(1, 0, n - 1, l, r); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    Segtree seg(n);
    seg.build(a);
    while (q--) {
        int t;
        cin >> t;
        if (t == 1) {
            int k;
            ll x;
            cin >> k >> x;
            seg.add(k - 1, x);
        } else {
            int l, r;
            cin >> l >> r;
            cout << seg.query(l - 1, r - 1) << '\n';
        }
    }
}

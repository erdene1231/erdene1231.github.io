#include <bits/stdc++.h>
using namespace std;

struct MinSegtree {
    int n;
    vector<int> tree;
    MinSegtree(int _n) {
        n = _n;
        tree.assign(n * 4 + 5, INT_MAX);
    }
    void build(int v, int tl, int tr, const vector<int>& a) {
        if (tl == tr) {
            tree[v] = a[tl];
            return;
        }
        int tm = (tl + tr) / 2;
        build(v * 2, tl, tm, a);
        build(v * 2 + 1, tm + 1, tr, a);
        tree[v] = min(tree[v * 2], tree[v * 2 + 1]);
    }
    void update(int v, int tl, int tr, int k, int x) {
        if (tl == tr) {
            tree[v] = x;
            return;
        }
        int tm = (tl + tr) / 2;
        if (k <= tm) update(v * 2, tl, tm, k, x);
        else update(v * 2 + 1, tm + 1, tr, k, x);
        tree[v] = min(tree[v * 2], tree[v * 2 + 1]);
    }
    int query(int v, int tl, int tr, int l, int r) const {
        if (r < tl || tr < l) return INT_MAX;
        if (l <= tl && tr <= r) return tree[v];
        int tm = (tl + tr) / 2;
        return min(query(v * 2, tl, tm, l, r), query(v * 2 + 1, tm + 1, tr, l, r));
    }
    int first_min(int v, int tl, int tr) const {
        if (tl == tr) return tl;
        int tm = (tl + tr) / 2;
        if (tree[v * 2] <= tree[v * 2 + 1]) return first_min(v * 2, tl, tm);
        return first_min(v * 2 + 1, tm + 1, tr);
    }
    void build(const vector<int>& a) { build(1, 0, n - 1, a); }
    void update(int k, int x) { update(1, 0, n - 1, k, x); }
    int query(int l, int r) const { return query(1, 0, n - 1, l, r); }
    int first_min() const { return first_min(1, 0, n - 1); }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    MinSegtree seg(n);
    seg.build(a);
    while (q--) {
        int t;
        cin >> t;
        if (t == 1) {
            int k, x;
            cin >> k >> x;
            seg.update(k - 1, x);
        } else if (t == 2) {
            int l, r;
            cin >> l >> r;
            cout << seg.query(l - 1, r - 1) << '\n';
        } else cout << seg.first_min() + 1 << '\n';
    }
}

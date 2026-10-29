#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Segtree {
    int n;
    vector<ll> tree, add, setval;
    vector<bool> has;

    Segtree(int _n) {
        n = _n;
        tree.resize(n * 4 + 5);
        add.resize(n * 4 + 5);
        setval.resize(n * 4 + 5);
        has.resize(n * 4 + 5, false);
    }

    void build(int v, int tl, int tr, const vector<ll> &a) {
        if (tr - tl == 1) tree[v] = a[tl];
        else {
            int tm = (tl + tr) / 2;
            build(v * 2, tl, tm, a);
            build(v * 2 + 1, tm, tr, a);
            tree[v] = tree[v * 2] + tree[v * 2 + 1];
        }
    }
    void applySet(int v, int len, ll x) {
        tree[v] = x * len;
        setval[v] = x;
        has[v] = true;
        add[v] = 0;
    }

    void applyAdd(int v, int len, ll x) {
        tree[v] += x * len;
        add[v] += x;
    }

    void push(int v, int tl, int tr) {
        if (tr - tl == 1) return;
        int tm = (tl + tr) / 2;
        if (has[v]) {
            applySet(v * 2, tm - tl, setval[v]);
            applySet(v * 2 + 1, tr - tm, setval[v]);
            has[v] = false;
        }
        if (add[v] != 0) {
            applyAdd(v * 2, tm - tl, add[v]);
            applyAdd(v * 2 + 1, tr - tm, add[v]);
            add[v] = 0;
        }
    }
    void update(int v, int tl, int tr, int l, int r, ll x, bool assign) {
        if (r <= tl || tr <= l) return;
        if (l <= tl && tr <= r) {
            if (assign) applySet(v, tr - tl, x);
            else applyAdd(v, tr - tl, x);
            return;
        }
        push(v, tl, tr);
        int tm = (tl + tr) / 2;
        update(v * 2, tl, tm, l, r, x, assign);
        update(v * 2 + 1, tm, tr, l, r, x, assign);
        tree[v] = tree[v * 2] + tree[v * 2 + 1];
    }

    ll query(int v, int tl, int tr, int l, int r) {
        if (r <= tl || tr <= l) return 0;
        if (l <= tl && tr <= r) return tree[v];
        push(v, tl, tr);
        int tm = (tl + tr) / 2;
        return query(v * 2, tl, tm, l, r) + query(v * 2 + 1, tm, tr, l, r);
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    Segtree st(n);
    st.build(1, 0, n, a);
    while (q--) {
        int type, l, r;
        cin >> type >> l >> r;
        if (type == 3) cout << st.query(1, 0, n, l, r) << '\n';
        else {
            ll x;
            cin >> x;
            st.update(1, 0, n, l, r, x, type == 2);
        }
    }
}

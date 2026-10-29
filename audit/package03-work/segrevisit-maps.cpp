#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Segtree {
    int n;
    vector<ll> a;
    vector<map<ll, int>> tree;

    Segtree(const vector<ll> &v) {
        a = v;
        n = (int) a.size();
        tree.resize(n * 4 + 5);
        build(1, 0, n);
    }

    void build(int v, int tl, int tr) {
        if (tr - tl == 1) tree[v][a[tl]] = 1;
        else {
            int tm = (tl + tr) / 2;
            build(v * 2, tl, tm);
            build(v * 2 + 1, tm, tr);
            for (auto [x, count] : tree[v * 2]) tree[v][x] += count;
            for (auto [x, count] : tree[v * 2 + 1]) tree[v][x] += count;
        }
    }
    void update(int v, int tl, int tr, int i, ll x) {
        auto it = tree[v].find(a[i]);
        if (--it->second == 0) tree[v].erase(it);
        tree[v][x]++;
        if (tr - tl == 1) a[i] = x;
        else {
            int tm = (tl + tr) / 2;
            if (i < tm) update(v * 2, tl, tm, i, x);
            else update(v * 2 + 1, tm, tr, i, x);
        }
    }

    int query(int v, int tl, int tr, int l, int r, ll x) const {
        if (r <= tl || tr <= l) return 0;
        if (l <= tl && tr <= r) {
            auto it = tree[v].find(x);
            return it == tree[v].end() ? 0 : it->second;
        }
        int tm = (tl + tr) / 2;
        return query(v * 2, tl, tm, l, r, x) + query(v * 2 + 1, tm, tr, l, r, x);
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    Segtree st(a);
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int i;
            ll x;
            cin >> i >> x;
            st.update(1, 0, n, i, x);
        } else {
            int l, r;
            ll x;
            cin >> l >> r >> x;
            cout << st.query(1, 0, n, l, r, x) << '\n';
        }
    }
}

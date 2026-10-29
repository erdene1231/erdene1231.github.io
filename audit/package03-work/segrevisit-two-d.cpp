#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Segtree2D {
    int n, m;
    vector<vector<ll>> tree;

    Segtree2D(int _n, int _m) {
        n = _n;
        m = _m;
        tree.assign(n * 4 + 5, vector<ll>(m * 4 + 5));
    }

    void buildY(int vx, int tl, int tr, int vy, int cl, int cr, const vector<vector<ll>> &a) {
        if (cr - cl == 1) {
            if (tr - tl == 1) tree[vx][vy] = a[tl][cl];
            else tree[vx][vy] = tree[vx * 2][vy] + tree[vx * 2 + 1][vy];
        } else {
            int cm = (cl + cr) / 2;
            buildY(vx, tl, tr, vy * 2, cl, cm, a);
            buildY(vx, tl, tr, vy * 2 + 1, cm, cr, a);
            tree[vx][vy] = tree[vx][vy * 2] + tree[vx][vy * 2 + 1];
        }
    }

    void buildX(int v, int tl, int tr, const vector<vector<ll>> &a) {
        if (tr - tl > 1) {
            int tm = (tl + tr) / 2;
            buildX(v * 2, tl, tm, a);
            buildX(v * 2 + 1, tm, tr, a);
        }
        buildY(v, tl, tr, 1, 0, m, a);
    }
    void updateY(int vx, int tl, int tr, int vy, int cl, int cr, int col, ll x) {
        if (cr - cl == 1) {
            if (tr - tl == 1) tree[vx][vy] = x;
            else tree[vx][vy] = tree[vx * 2][vy] + tree[vx * 2 + 1][vy];
        } else {
            int cm = (cl + cr) / 2;
            if (col < cm) updateY(vx, tl, tr, vy * 2, cl, cm, col, x);
            else updateY(vx, tl, tr, vy * 2 + 1, cm, cr, col, x);
            tree[vx][vy] = tree[vx][vy * 2] + tree[vx][vy * 2 + 1];
        }
    }

    void updateX(int v, int tl, int tr, int row, int col, ll x) {
        if (tr - tl > 1) {
            int tm = (tl + tr) / 2;
            if (row < tm) updateX(v * 2, tl, tm, row, col, x);
            else updateX(v * 2 + 1, tm, tr, row, col, x);
        }
        updateY(v, tl, tr, 1, 0, m, col, x);
    }
    ll queryY(int vx, int v, int tl, int tr, int l, int r) const {
        if (r <= tl || tr <= l) return 0;
        if (l <= tl && tr <= r) return tree[vx][v];
        int tm = (tl + tr) / 2;
        return queryY(vx, v * 2, tl, tm, l, r) + queryY(vx, v * 2 + 1, tm, tr, l, r);
    }

    ll queryX(int v, int tl, int tr, int l, int r, int cl, int cr) const {
        if (r <= tl || tr <= l) return 0;
        if (l <= tl && tr <= r) return queryY(v, 1, 0, m, cl, cr);
        int tm = (tl + tr) / 2;
        return queryX(v * 2, tl, tm, l, r, cl, cr) + queryX(v * 2 + 1, tm, tr, l, r, cl, cr);
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, q;
    cin >> n >> m >> q;
    vector<vector<ll>> a(n, vector<ll>(m));
    for (auto &row : a) for (ll &x : row) cin >> x;
    Segtree2D st(n, m);
    st.buildX(1, 0, n, a);
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int r, c;
            ll x;
            cin >> r >> c >> x;
            st.updateX(1, 0, n, r, c, x);
        } else {
            int l, r, cl, cr;
            cin >> l >> r >> cl >> cr;
            cout << st.queryX(1, 0, n, l, r, cl, cr) << '\n';
        }
    }
}

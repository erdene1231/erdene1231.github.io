#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll MOD = 1000000007;
using Coeff = array<ll, 6>;

struct Segtree {
    int n, k;
    vector<ll> tree;
    vector<Coeff> lazy;
    vector<vector<ll>> moment;
    ll choose[6][6]{};

    Segtree(int _n, int _k) {
        n = _n;
        k = _k;
        tree.resize(n * 4 + 5);
        lazy.resize(n * 4 + 5);
        moment.assign(k + 1, vector<ll>(n + 1));
        for (int i = 0; i <= k; i++) {
            choose[i][0] = choose[i][i] = 1;
            for (int j = 1; j < i; j++) choose[i][j] = choose[i - 1][j - 1] + choose[i - 1][j];
        }
        for (int u = 0; u < n; u++) {
            ll power = 1;
            for (int j = 0; j <= k; j++) {
                moment[j][u + 1] = (moment[j][u] + power) % MOD;
                power = power * u % MOD;
            }
        }
    }

    void build(int v, int tl, int tr, const vector<ll> &a) {
        if (tr - tl == 1) tree[v] = (a[tl] % MOD + MOD) % MOD;
        else {
            int tm = (tl + tr) / 2;
            build(v * 2, tl, tm, a);
            build(v * 2 + 1, tm, tr, a);
            tree[v] = (tree[v * 2] + tree[v * 2 + 1]) % MOD;
        }
    }
    Coeff shift(const Coeff &c, int h) {
        Coeff result{}, power{};
        power[0] = 1;
        for (int i = 1; i <= k; i++) power[i] = power[i - 1] * h % MOD;
        for (int i = 0; i <= k; i++) {
            for (int j = 0; j <= i; j++) {
                ll term = c[i] * choose[i][j] % MOD * power[i - j] % MOD;
                result[j] = (result[j] + term) % MOD;
            }
        }
        return result;
    }

    void apply(int v, int len, const Coeff &c) {
        for (int j = 0; j <= k; j++) {
            tree[v] = (tree[v] + c[j] * moment[j][len]) % MOD;
            lazy[v][j] = (lazy[v][j] + c[j]) % MOD;
        }
    }

    void push(int v, int tl, int tr) {
        if (tr - tl == 1 || lazy[v] == Coeff{}) return;
        int tm = (tl + tr) / 2;
        apply(v * 2, tm - tl, lazy[v]);
        apply(v * 2 + 1, tr - tm, shift(lazy[v], tm - tl));
        lazy[v] = Coeff{};
    }
    void update(int v, int tl, int tr, int l, int r, const Coeff &c) {
        if (r <= tl || tr <= l) return;
        if (l <= tl && tr <= r) {
            apply(v, tr - tl, shift(c, tl - l));
            return;
        }
        push(v, tl, tr);
        int tm = (tl + tr) / 2;
        update(v * 2, tl, tm, l, r, c);
        update(v * 2 + 1, tm, tr, l, r, c);
        tree[v] = (tree[v * 2] + tree[v * 2 + 1]) % MOD;
    }

    ll query(int v, int tl, int tr, int l, int r) {
        if (r <= tl || tr <= l) return 0;
        if (l <= tl && tr <= r) return tree[v];
        push(v, tl, tr);
        int tm = (tl + tr) / 2;
        return (query(v * 2, tl, tm, l, r) + query(v * 2 + 1, tm, tr, l, r)) % MOD;
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, k;
    cin >> n >> q >> k;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    Segtree st(n, k);
    st.build(1, 0, n, a);
    while (q--) {
        int type, l, r;
        cin >> type >> l >> r;
        if (type == 2) cout << st.query(1, 0, n, l, r) << '\n';
        else {
            Coeff c{};
            for (int j = 0; j <= k; j++) {
                cin >> c[j];
                c[j] = (c[j] % MOD + MOD) % MOD;
            }
            st.update(1, 0, n, l, r, c);
        }
    }
}

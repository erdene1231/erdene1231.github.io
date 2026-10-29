#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll scan(const vector<int>& a, int l, int r) {
    ll s = 0;
    for (int i = l; i <= r; i++) s += a[i];
    return s;
}

struct Prefix {
    int n;
    vector<ll> p;
    Prefix(int _n) {
        n = _n;
        p.resize(n + 1);
    }
    void build(const vector<int>& a) {
        for (int i = 0; i < n; i++) p[i + 1] = p[i] + a[i];
    }
    ll sum(int l, int r) const {
        return p[r + 1] - p[l];
    }
};

struct Sparse {
    int n;
    vector<int> lg;
    vector<vector<int>> st;
    Sparse(int _n) {
        n = _n;
        lg.resize(n + 1);
        for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;
        st.assign(lg[n] + 1, vector<int>(n));
    }
    void build(const vector<int>& a) {
        st[0] = a;
        for (int j = 1; (1 << j) <= n; j++) {
            for (int i = 0; i + (1 << j) <= n; i++) {
                st[j][i] = min(st[j - 1][i], st[j - 1][i + (1 << (j - 1))]);
            }
        }
    }
    int query(int l, int r) const {
        int j = lg[r - l + 1];
        return min(st[j][l], st[j][r - (1 << j) + 1]);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    Prefix pref(n);
    Sparse rmq(n);
    pref.build(a);
    rmq.build(a);
    while (q--) {
        int t, l, r;
        cin >> t >> l >> r;
        --l;
        --r;
        if (t == 1) cout << pref.sum(l, r) << '\n';
        else if (t == 2) cout << rmq.query(l, r) << '\n';
        else cout << scan(a, l, r) << '\n';
    }
}

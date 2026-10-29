#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct IterSegtree {
    int n;
    vector<ll> tree;
    IterSegtree(int _n) {
        n = 1;
        while (n < _n) n *= 2;
        tree.resize(n * 2);
    }
    void build(const vector<int>& a) {
        for (int i = 0; i < (int)a.size(); i++) tree[n + i] = a[i];
        for (int v = n - 1; v > 0; v--) tree[v] = tree[v * 2] + tree[v * 2 + 1];
    }
    void add(int k, ll x) {
        k += n;
        tree[k] += x;
        for (k /= 2; k > 0; k /= 2) tree[k] = tree[k * 2] + tree[k * 2 + 1];
    }
    ll query(int l, int r) const {
        l += n;
        r += n;
        ll s = 0;
        while (l <= r) {
            if (l % 2 == 1) s += tree[l++];
            if (r % 2 == 0) s += tree[r--];
            l /= 2;
            r /= 2;
        }
        return s;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    IterSegtree seg(n);
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

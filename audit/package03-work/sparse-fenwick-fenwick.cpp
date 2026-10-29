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

    void add(int i, ll x) {
        for (; i <= n; i += i & -i) tree[i] += x;
    }

    ll sum(int i) const {
        ll s = 0;
        for (; i > 0; i -= i & -i) s += tree[i];
        return s;
    }

    ll rangeSum(int l, int r) const {
        return sum(r) - sum(l - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n + 1);
    Fenwick fw(n);
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        fw.add(i, a[i]);
    }
    while (q--) {
        int type, l, r;
        cin >> type;
        if (type == 1) {
            ll x;
            cin >> l >> x;
            fw.add(l, x - a[l]);
            a[l] = x;
        } else {
            cin >> l >> r;
            cout << fw.rangeSum(l, r) << '\n';
        }
    }
    return 0;
}

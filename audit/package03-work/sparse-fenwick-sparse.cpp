#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Sparse {
    int n;
    vector<int> lg;
    vector<vector<ll>> st;

    Sparse(int _n) {
        n = _n;
        lg.resize(n + 1);
        for (int i = 2; i <= n; i++) lg[i] = lg[i / 2] + 1;
        int k = n ? lg[n] + 1 : 0;
        st.assign(k, vector<ll>(n));
    }

    void build(const vector<ll> &a) {
        if (n == 0) return;
        st[0] = a;
        for (int k = 1; k < (int)st.size(); k++) {
            int w = 1 << (k - 1);
            for (int i = 0; i + 2 * w <= n; i++) {
                st[k][i] = min(st[k - 1][i], st[k - 1][i + w]);
            }
        }
    }

    ll query(int l, int r) const {
        int k = lg[r - l];
        int w = 1 << k;
        return min(st[k][l], st[k][r - w]);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    Sparse sp(n);
    sp.build(a);
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << sp.query(l - 1, r) << '\n';
    }
    return 0;
}

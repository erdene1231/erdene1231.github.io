#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Node {
    ll sum = 0;
    int left = 0, right = 0;
};

struct Sparse {
    ll n;
    vector<Node> tree;

    Sparse(ll _n) {
        n = _n;
        tree.resize(2);
    }

    int create() {
        tree.push_back(Node{});
        return (int) tree.size() - 1;
    }
    void update(int v, ll tl, ll tr, ll i, ll x) {
        if (tr - tl == 1) {
            tree[v].sum = x;
            return;
        }
        ll tm = tl + (tr - tl) / 2;
        if (i < tm) {
            if (!tree[v].left) {
                int u = create();
                tree[v].left = u;
            }
            update(tree[v].left, tl, tm, i, x);
        } else {
            if (!tree[v].right) {
                int u = create();
                tree[v].right = u;
            }
            update(tree[v].right, tm, tr, i, x);
        }
        tree[v].sum = tree[tree[v].left].sum + tree[tree[v].right].sum;
    }

    ll query(int v, ll tl, ll tr, ll l, ll r) const {
        if (!v || r <= tl || tr <= l) return 0;
        if (l <= tl && tr <= r) return tree[v].sum;
        ll tm = tl + (tr - tl) / 2;
        return query(tree[v].left, tl, tm, l, r) + query(tree[v].right, tm, tr, l, r);
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll n;
    int q;
    cin >> n >> q;
    Sparse st(n);
    while (q--) {
        int type;
        ll l, x;
        cin >> type >> l >> x;
        if (type == 1) st.update(1, 0, n, l, x);
        else cout << st.query(1, 0, n, l, x) << '\n';
    }
}

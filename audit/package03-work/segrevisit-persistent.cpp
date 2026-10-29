#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Node {
    ll sum = 0;
    int left = 0, right = 0;
};

struct Persistent {
    int n;
    vector<Node> tree;
    vector<int> roots;

    Persistent(int _n) {
        n = _n;
        tree.push_back(Node{});
        roots.push_back(build(0, n));
    }

    int build(int tl, int tr) {
        int v = (int) tree.size();
        tree.push_back(Node{});
        if (tr - tl > 1) {
            int tm = (tl + tr) / 2;
            int left = build(tl, tm);
            int right = build(tm, tr);
            tree[v].left = left;
            tree[v].right = right;
        }
        return v;
    }
    int update(int old, int tl, int tr, int i, ll x) {
        Node copy = tree[old];
        tree.push_back(copy);
        int v = (int) tree.size() - 1;
        if (tr - tl == 1) tree[v].sum = x;
        else {
            int tm = (tl + tr) / 2;
            if (i < tm) {
                int u = update(tree[v].left, tl, tm, i, x);
                tree[v].left = u;
            } else {
                int u = update(tree[v].right, tm, tr, i, x);
                tree[v].right = u;
            }
            tree[v].sum = tree[tree[v].left].sum + tree[tree[v].right].sum;
        }
        return v;
    }

    ll query(int v, int tl, int tr, int l, int r) const {
        if (!v || r <= tl || tr <= l) return 0;
        if (l <= tl && tr <= r) return tree[v].sum;
        int tm = (tl + tr) / 2;
        return query(tree[v].left, tl, tm, l, r) + query(tree[v].right, tm, tr, l, r);
    }
    int assign(int version, int i, ll x) {
        int root = update(roots[version], 0, n, i, x);
        roots.push_back(root);
        return (int) roots.size() - 1;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    Persistent st(n);
    while (q--) {
        int type, version, l;
        ll x;
        cin >> type >> version >> l >> x;
        if (type == 1) cout << st.assign(version, l, x) << '\n';
        else cout << st.query(st.roots[version], 0, n, l, (int) x) << '\n';
    }
}

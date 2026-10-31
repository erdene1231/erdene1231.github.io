#include <bits/stdc++.h>
using namespace std;

struct SegmentTree {
    int n;
    vector<int> mx, lazy;
    SegmentTree(int width) : n(1) {
        while (n < width) n *= 2;
        mx.assign(2 * n, 0);
        lazy.assign(2 * n, -1);
    }
    void apply(int node, int value) {
        mx[node] = lazy[node] = value;
    }
    void push(int node) {
        if (lazy[node] == -1) return;
        apply(node * 2, lazy[node]);
        apply(node * 2 + 1, lazy[node]);
        lazy[node] = -1;
    }
    int query(int node, int left, int right, int ql, int qr) {
        if (qr <= left || right <= ql) return 0;
        if (ql <= left && right <= qr) return mx[node];
        push(node);
        int mid = (left + right) / 2;
        return max(query(node * 2, left, mid, ql, qr), query(node * 2 + 1, mid, right, ql, qr));
    }
    void assign(int node, int left, int right, int ql, int qr, int value) {
        if (qr <= left || right <= ql) return;
        if (ql <= left && right <= qr) {
            apply(node, value);
            return;
        }
        push(node);
        int mid = (left + right) / 2;
        assign(node * 2, left, mid, ql, qr, value);
        assign(node * 2 + 1, mid, right, ql, qr, value);
        mx[node] = max(mx[node * 2], mx[node * 2 + 1]);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int w, n;
    cin >> w >> n;
    SegmentTree tree(w);
    while (n--) {
        int l, r;
        cin >> l >> r;
        --l;
        int height = tree.query(1, 0, tree.n, l, r) + 1;
        tree.assign(1, 0, tree.n, l, r, height);
        cout << height << '\n';
    }
}

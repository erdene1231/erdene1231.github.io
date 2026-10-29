#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Query {
    int l, r, id;
};

struct Mo {
    int n, b, distinct = 0;
    vector<int> a, count;

    Mo(const vector<ll> &v) {
        n = (int) v.size();
        b = max(1, (int) sqrt(n));
        vector<ll> vals = v;
        sort(vals.begin(), vals.end());
        vals.erase(unique(vals.begin(), vals.end()), vals.end());
        count.assign(vals.size(), 0);
        for (ll x : v) {
            a.push_back((int) (lower_bound(vals.begin(), vals.end(), x) - vals.begin()));
        }
    }
    void add(int i) {
        if (++count[a[i]] == 1) distinct++;
    }

    void remove(int i) {
        if (--count[a[i]] == 0) distinct--;
    }

    vector<int> solve(vector<Query> queries) {
        sort(queries.begin(), queries.end(), [&](Query x, Query y) {
            if (x.l / b != y.l / b) return x.l / b < y.l / b;
            return x.r < y.r;
        });
        fill(count.begin(), count.end(), 0);
        distinct = 0;
        vector<int> ans(queries.size());
        int l = 0, r = 0;
        for (auto [ql, qr, id] : queries) {
            while (l > ql) add(--l);
            while (r < qr) add(r++);
            while (l < ql) remove(l++);
            while (r > qr) remove(--r);
            ans[id] = distinct;
        }
        return ans;
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    vector<Query> queries(q);
    for (int i = 0; i < q; i++) {
        cin >> queries[i].l >> queries[i].r;
        queries[i].id = i;
    }
    Mo st(a);
    for (int ans : st.solve(queries)) cout << ans << '\n';
}

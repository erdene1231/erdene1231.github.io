#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Fenwick {
    int n;
    vector<int> tree;

    Fenwick(int _n) {
        n = _n;
        tree.resize(n + 1);
    }

    void add(int i, int x) {
        for (i++; i <= n; i += i & -i) tree[i] += x;
    }

    int sum(int r) const {
        int ans = 0;
        for (; r > 0; r -= r & -r) ans += tree[r];
        return ans;
    }
};

struct Seg {
    ll line, l, r;
    bool operator<(const Seg &s) const {
        return tie(line, l, r) < tie(s.line, s.l, s.r);
    }
};

struct Event {
    ll x;
    int type;
    ll l, r;
    bool operator<(const Event &e) const {
        return tie(x, type, l, r) < tie(e.x, e.type, e.l, e.r);
    }
};
vector<Seg> unite(vector<Seg> a) {
    sort(a.begin(), a.end());
    vector<Seg> result;
    for (Seg s : a) {
        if (!result.empty() && result.back().line == s.line && s.l <= result.back().r) {
            result.back().r = max(result.back().r, s.r);
        } else result.push_back(s);
    }
    return result;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string mode;
    int n;
    cin >> mode >> n;
    vector<Seg> h, v;
    for (int i = 0; i < n; i++) {
        char type;
        ll a, b, c;
        cin >> type >> a >> b >> c;
        if (type == 'H') h.push_back({c, min(a, b), max(a, b)});
        else v.push_back({a, min(b, c), max(b, c)});
    }
    if (mode == "POINTS") {
        h = unite(h);
        v = unite(v);
    }
    vector<ll> ys;
    vector<Event> events;
    for (Seg s : h) {
        ys.push_back(s.line);
        events.push_back({s.l, 0, s.line, s.line});
        events.push_back({s.r, 2, s.line, s.line});
    }
    for (Seg s : v) events.push_back({s.line, 1, s.l, s.r});
    sort(ys.begin(), ys.end());
    ys.erase(unique(ys.begin(), ys.end()), ys.end());
    sort(events.begin(), events.end());
    Fenwick st((int) ys.size());
    ll ans = 0;
    for (Event e : events) {
        if (e.type == 1) {
            int l = (int) (lower_bound(ys.begin(), ys.end(), e.l) - ys.begin());
            int r = (int) (upper_bound(ys.begin(), ys.end(), e.r) - ys.begin());
            ans += st.sum(r) - st.sum(l);
        } else {
            int i = (int) (lower_bound(ys.begin(), ys.end(), e.l) - ys.begin());
            st.add(i, e.type == 0 ? 1 : -1);
        }
    }
    cout << ans << '\n';
}

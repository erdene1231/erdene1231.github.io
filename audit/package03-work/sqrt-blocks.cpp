#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct SqrtSum {
    int n, b;
    vector<ll> a, sum;

    SqrtSum(vector<ll> v) {
        a = move(v);
        n = (int) a.size();
        b = max(1, (int) sqrt(n));
        sum.assign((n + b - 1) / b, 0);
        for (int i = 0; i < n; i++) sum[i / b] += a[i];
    }
    void update(int i, ll x) {
        sum[i / b] += x - a[i];
        a[i] = x;
    }

    ll query(int l, int r) {
        ll ans = 0;
        while (l < r && l % b) ans += a[l++];
        while (r - l >= b) {
            ans += sum[l / b];
            l += b;
        }
        while (l < r) ans += a[l++];
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
    SqrtSum st(a);
    while (q--) {
        int type, l;
        ll x;
        cin >> type >> l >> x;
        if (type == 1) st.update(l, x);
        else cout << st.query(l, (int) x) << '\n';
    }
}

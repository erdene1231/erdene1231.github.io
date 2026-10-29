#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<ll> prefix(const vector<ll> &a) {
    int n = a.size();
    vector<ll> p(n + 1);
    for (int i = 0; i < n; i++) p[i + 1] = p[i] + a[i];
    return p;
}

ll rangeSum(const vector<ll> &p, int l, int r) {
    return p[r] - p[l];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    vector<ll> p = prefix(a);
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << rangeSum(p, l - 1, r) << '\n';
    }
    return 0;
}

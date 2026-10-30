#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<ll> sums(const vector<ll> &a) {
    vector<ll> s = {0};
    s.reserve(1ULL << a.size());
    for (ll x : a) {
        int k = (int)s.size();
        for (int i = 0; i < k; i++) s.push_back(s[i] + x);
    }
    return s;
}

ll count_meet(const vector<ll> &a, ll t) {
    int m = (int)a.size() / 2;
    auto l = sums(vector<ll>(a.begin(), a.begin() + m));
    auto r = sums(vector<ll>(a.begin() + m, a.end()));
    sort(r.begin(), r.end());
    ll ans = 0;
    for (ll s : l) {
        auto [p, q] = equal_range(r.begin(), r.end(), t - s);
        ans += (ll)(q - p);
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll t;
    cin >> n >> t;
    assert(0 <= n && n <= 40);
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    cout << count_meet(a, t) << '\n';
}

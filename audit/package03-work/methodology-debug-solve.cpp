#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll fast(const vector<ll> &a) {
    int n = (int)a.size();
    assert(n > 0);
    vector<ll> f(n, 0);
    f[0] = 1;
    ll s = 0, ans = 0;
    for (ll x : a) {
        s = (s + x) % n;
        if (s < 0) s += n;
        assert(0 <= s && s < n);
        ans += f[s];
        f[s]++;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    assert(1 <= n && n <= 200000);
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    cout << fast(a) << '\n';
}

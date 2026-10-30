#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll submaskSum(const vector<ll> &v, int s) {
    ll ans = 0;
    for (int t = s; ; t = (t - 1) & s) {
        ans += v[t];
        if (t == 0) break;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, s;
    cin >> n >> s;
    int m = 1 << n;
    vector<ll> v(m);
    for (ll &x : v) cin >> x;
    cout << submaskSum(v, s) << '\n';
    return 0;
}

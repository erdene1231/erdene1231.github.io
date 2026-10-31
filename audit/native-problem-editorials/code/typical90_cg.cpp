#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll k;
    cin >> k;
    vector<ll> divisors;
    for (ll d = 1; d <= k / d; ++d) {
        if (k % d != 0) continue;
        divisors.push_back(d);
        if (d != k / d) divisors.push_back(k / d);
    }
    sort(divisors.begin(), divisors.end());
    ll ans = 0;
    for (int i = 0; i < int(divisors.size()); ++i) {
        ll a = divisors[i], rem = k / a;
        if (a > rem / a) break;
        for (int j = i; j < int(divisors.size()); ++j) {
            ll b = divisors[j];
            if (b > rem / b) break;
            if (rem % b == 0) ++ans;
        }
    }
    cout << ans << '\n';
}

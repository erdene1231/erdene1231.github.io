#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<ll> gain;
    gain.reserve(2 * n);
    for (int i = 0; i < n; ++i) {
        ll a, b;
        cin >> a >> b;
        gain.push_back(b);
        gain.push_back(a - b);
    }
    sort(gain.begin(), gain.end(), greater<ll>());
    ll ans = 0;
    for (int i = 0; i < k; ++i) ans += gain[i];
    cout << ans << '\n';
}

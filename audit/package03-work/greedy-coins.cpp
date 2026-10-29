#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll n;
    if (!(cin >> n)) return 0;
    vector<int> c = {200, 100, 50, 20, 10, 5, 2, 1};
    ll ans = 0;
    for (int x : c) {
        ll cnt = n / x;
        ans += cnt;
        n %= x;
        cout << x << ' ' << cnt << '\n';
    }
    cout << ans << '\n';
}

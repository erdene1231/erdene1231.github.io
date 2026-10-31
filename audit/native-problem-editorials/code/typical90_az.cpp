#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    const ll mod = 1000000007;
    ll ans = 1;
    for (int i = 0; i < n; ++i) {
        int sum = 0;
        for (int j = 0; j < 6; ++j) {
            int x;
            cin >> x;
            sum += x;
        }
        ans = ans * sum % mod;
    }
    cout << ans << '\n';
}

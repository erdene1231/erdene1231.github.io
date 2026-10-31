#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll mod = 1000000007;

ll power(ll a, ll e) {
    ll result = 1;
    while (e > 0) {
        if (e & 1) result = result * a % mod;
        a = a * a % mod;
        e >>= 1;
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll n, k;
    cin >> n >> k;
    if (n == 1) cout << k % mod << '\n';
    else if (n == 2) cout << k * (k - 1) % mod << '\n';
    else if (k < 3) cout << 0 << '\n';
    else cout << k * (k - 1) % mod * power(k - 2, n - 2) % mod << '\n';
}

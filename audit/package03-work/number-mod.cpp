#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll norm(ll x, int m) {
    x %= m;
    if (x < 0) x += m;
    return x;
}

ll modpow(ll x, ll n, int m) {
    x = norm(x, m);
    if (n == 0) return 1 % m;
    ll u = modpow(x, n / 2, m);
    u = u * u % m;
    if (n % 2) u = u * x % m;
    return u;
}

int phi(int n) {
    int res = n;
    for (int p = 2; p <= n / p; p++) {
        if (n % p) continue;
        while (n % p == 0) n /= p;
        res = res / p * (p - 1);
    }
    if (n > 1) res = res / n * (n - 1);
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll x, n;
    int m;
    cin >> x >> n >> m; // n >= 0, 1 <= m <= INT_MAX
    cout << modpow(x, n, m) << "\n";
    ll a = norm(x, m);
    if (m == 1 || gcd(a, (ll)m) != 1) {
        cout << "NO INVERSE\n";
    } else {
        cout << modpow(a, phi(m) - 1, m) << "\n";
    }
    uint32_t u = 123456789;
    uint32_t v = uint32_t(uint64_t(u) * u);
    cout << v << "\n";
}

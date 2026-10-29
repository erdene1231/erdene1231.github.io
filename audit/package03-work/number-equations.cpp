#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll exgcd(ll a, ll b, ll &x, ll &y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    ll u, v;
    ll g = exgcd(b, a % b, u, v);
    x = v;
    y = u - (a / b) * v;
    return g;
}

ll norm(ll x, ll m) {
    x %= m;
    if (x < 0) x += m;
    return x;
}

bool crt(const vector<ll> &a, const vector<ll> &m, ll &x, ll &mod) {
    mod = 1;
    for (int i = 0; i < (int)m.size(); i++) {
        if (m[i] < 2 || mod > 1000000000 / m[i]) return false;
        for (int j = 0; j < i; j++) {
            if (gcd(m[i], m[j]) != 1) return false;
        }
        mod *= m[i];
    }
    x = 0;
    for (int i = 0; i < (int)m.size(); i++) {
        ll part = mod / m[i], u, v;
        exgcd(part, m[i], u, v);
        ll term = norm(a[i], m[i]) * part % mod;
        term = term * norm(u, m[i]) % mod;
        x = (x + term) % mod;
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    char mode;
    cin >> mode;
    if (mode == 'D') {
        ll a, b, c, x, y;
        cin >> a >> b >> c; // 1 <= a,b <= 10^9; |c| <= 10^9
        ll g = exgcd(a, b, x, y);
        if (c % g) cout << "NONE\n";
        else cout << x * (c / g) << ' ' << y * (c / g)
                  << ' ' << b / g << ' ' << -a / g << "\n";
    } else {
        int n;
        cin >> n; // 1 <= n <= 30; product of moduli <= 10^9
        vector<ll> a(n), m(n);
        for (int i = 0; i < n; i++) cin >> a[i] >> m[i];
        ll x, mod;
        if (!crt(a, m, x, mod)) cout << "UNSUPPORTED\n";
        else cout << x << ' ' << mod << "\n";
    }
}

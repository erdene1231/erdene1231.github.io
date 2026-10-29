#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MOD = 1000000007;

ll modpow(ll a, int n) {
    ll res = 1;
    while (n) {
        if (n & 1) res = res * a % MOD;
        a = a * a % MOD;
        n >>= 1;
    }
    return res;
}

struct Comb {
    int n;
    vector<ll> f, inv;

    Comb(int _n) {
        n = _n;
        f.resize(n + 1);
        inv.resize(n + 1);
        f[0] = 1;
        for (int i = 1; i <= n; i++) f[i] = f[i - 1] * i % MOD;
        inv[n] = modpow(f[n], MOD - 2);
        for (int i = n; i >= 1; i--) inv[i - 1] = inv[i] * i % MOD;
    }

    ll choose(int a, int b) {
        if (b < 0 || b > a) return 0;
        return f[a] * inv[b] % MOD * inv[a - b] % MOD;
    }
};

ll pascal(int n, int k) {
    if (k < 0 || k > n) return 0;
    vector<ll> c(k + 1);
    c[0] = 1;
    for (int i = 1; i <= n; i++) {
        for (int j = min(i, k); j >= 1; j--) {
            c[j] = (c[j] + c[j - 1]) % MOD;
        }
    }
    return c[k];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    char mode;
    cin >> mode;
    if (mode == 'M') {
        int m, n = 0;
        cin >> m;
        vector<int> k(m);
        for (int &x : k) {
            cin >> x;
            n += x;
        }
        Comb c(n); // sum(k) <= 10^6, every k[i] >= 0
        ll ans = c.f[n];
        for (int x : k) ans = ans * c.inv[x] % MOD;
        cout << ans << "\n";
    } else {
        int n, k;
        cin >> n >> k;
        if (mode == 'P') { // 0 <= n <= 2000
            cout << pascal(n, k) << "\n";
        } else {
            Comb c(n + max(k, 0)); // 0 <= n,k; n+k <= 10^6
            if (mode == 'B') cout << c.choose(n, k) << "\n";
            else { // X: n >= 1; k >= 0
                cout << c.choose(n, k) << ' ' << c.choose(n + k - 1, k)
                     << ' ' << (k == 0 ? 1 : c.choose(n - k + 1, k)) << "\n";
            }
        }
    }
}

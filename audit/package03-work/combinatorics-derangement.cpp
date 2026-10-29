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

ll recurrence(int n) {
    ll a = 1, b = 0;
    if (n == 0) return a;
    for (int i = 2; i <= n; i++) {
        ll c = (i - 1) * (a + b) % MOD;
        a = b;
        b = c;
    }
    return b;
}

ll inclusion(int n) {
    vector<ll> inv(n + 1);
    ll f = 1;
    for (int i = 1; i <= n; i++) f = f * i % MOD;
    inv[n] = modpow(f, MOD - 2);
    for (int i = n; i >= 1; i--) inv[i - 1] = inv[i] * i % MOD;
    ll sum = 0;
    for (int k = 0; k <= n; k++) {
        if (k % 2) sum = (sum - inv[k] + MOD) % MOD;
        else sum = (sum + inv[k]) % MOD;
    }
    return f * sum % MOD;
}

int main() {
    int n;
    cin >> n; // 0 <= n <= 10^6 < MOD
    cout << recurrence(n) << ' ' << inclusion(n) << "\n";
}

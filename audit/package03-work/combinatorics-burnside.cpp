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

ll necklaces(int n, int m) {
    ll sum = 0;
    for (int k = 0; k < n; k++) {
        sum = (sum + modpow(m, gcd(k, n))) % MOD;
    }
    return sum * modpow(n, MOD - 2) % MOD;
}

int main() {
    int n, m;
    cin >> n >> m; // 1 <= n <= 10^6 < MOD; 1 <= m < MOD
    cout << necklaces(n, m) << "\n"; // rotations only, no reflection
}

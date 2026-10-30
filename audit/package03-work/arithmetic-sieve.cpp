#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Sieve {
    int n;
    vector<int> spf;
    Sieve(int _n) {
        n = _n;
        spf.assign(n + 1, 0);
        for (int p = 2; p <= n; p++) {
            if (spf[p]) continue;
            spf[p] = p;
            if (1LL * p * p > n) continue;
            for (ll j = 1LL * p * p; j <= n; j += p) {
                if (!spf[j]) spf[j] = p;
            }
        }
    }
    bool prime(int x) {
        return x >= 2 && spf[x] == x;
    }
    vector<pair<int, int>> factor(int x) {
        vector<pair<int, int>> f;
        while (x > 1) {
            int p = spf[x], e = 0;
            while (x % p == 0) {
                x /= p;
                e++;
            }
            f.push_back({p, e});
        }
        return f;
    }
    int divisors(int x) {
        int ans = 1;
        for (auto [p, e] : factor(x)) ans *= e + 1;
        return ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    Sieve s(n);
    while (q--) {
        int x;
        cin >> x;
        cout << s.prime(x) << ' ' << s.divisors(x) << '\n';
    }
}

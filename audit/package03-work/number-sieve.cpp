#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Sieve {
    int n;
    vector<int> f;

    Sieve(int _n) {
        n = _n;
        f.resize(n + 1);
        for (int x = 2; x <= n; x++) {
            if (f[x]) continue;
            for (int u = 2 * x; u <= n; u += x) {
                f[u] = x;
            }
        }
    }

    bool prime(int x) {
        return x >= 2 && f[x] == 0;
    }

    vector<int> factors(int x) {
        vector<int> res;
        while (x > 1) {
            int p = f[x] ? f[x] : x;
            res.push_back(p);
            x /= p;
        }
        sort(res.begin(), res.end());
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q; // 1 <= n <= 10^6; queries 1 <= x <= n
    Sieve s(n);
    for (int x = 2; x <= n; x++) cout << s.f[x] << " ";
    cout << "\n";
    while (q--) {
        int x;
        cin >> x;
        auto f = s.factors(x);
        cout << s.prime(x) << ' ' << f.size();
        for (int p : f) cout << ' ' << p;
        cout << "\n";
    }
}

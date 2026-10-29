#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool prime(int n) {
    if (n < 2) return false;
    for (int x = 2; x <= n / x; x++) {
        if (n % x == 0) return false;
    }
    return true;
}

vector<int> factors(int n) {
    vector<int> f;
    for (int x = 2; x <= n / x; x++) {
        while (n % x == 0) {
            f.push_back(x);
            n /= x;
        }
    }
    if (n > 1) f.push_back(n);
    return f;
}

struct Stats {
    ll cnt = 1, sum = 1, phi;
    ll prod = 1;
    bool fits = true;

    Stats(int n) {
        phi = n;
        vector<int> f = factors(n);
        vector<ll> divs = {1};
        for (int i = 0; i < (int)f.size();) {
            int p = f[i], j = i;
            while (j < (int)f.size() && f[j] == p) j++;
            ll pw = 1, s = 1;
            int len = divs.size();
            for (int k = i; k < j; k++) {
                pw *= p;
                s += pw;
                for (int u = 0; u < len; u++) {
                    divs.push_back(divs[u] * pw);
                }
            }
            cnt *= j - i + 1;
            sum *= s;
            phi = phi / p * (p - 1);
            i = j;
        }
        for (ll d : divs) {
            if (fits && prod <= LLONG_MAX / d) prod *= d;
            else fits = false;
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n; // 1 <= n <= 10^9
    auto f = factors(n);
    Stats s(n);
    cout << prime(n) << "\n";
    cout << f.size();
    for (int p : f) cout << ' ' << p;
    cout << "\n" << s.cnt << ' ' << s.sum << ' ' << s.phi << "\n";
    if (s.fits) cout << s.prod << "\n";
    else cout << "OVERFLOW\n";
}

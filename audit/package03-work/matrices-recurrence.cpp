#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MOD = 1000000007;

ll norm(ll x) {
    x %= MOD;
    if (x < 0) x += MOD;
    return x;
}

struct Mat {
    int n;
    vector<vector<ll>> a;

    Mat(int _n, bool unit = false) {
        n = _n;
        a.assign(n, vector<ll>(n));
        if (unit) for (int i = 0; i < n; i++) a[i][i] = 1;
    }

    Mat operator*(const Mat &b) const {
        Mat res(n);
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                for (int j = 0; j < n; j++) {
                    res.a[i][j] = (res.a[i][j] + a[i][k] * b.a[k][j]) % MOD;
                }
            }
        }
        return res;
    }
};

Mat power(Mat a, ll k) {
    Mat res(a.n, true);
    while (k) {
        if (k & 1) res = res * a;
        a = a * a;
        k >>= 1;
    }
    return res;
}

int main() {
    int k;
    ll n;
    cin >> k >> n; // 1 <= k <= 50; 0 <= n <= 10^18
    vector<ll> f(k), c(k);
    for (ll &x : f) {
        cin >> x;
        x = norm(x);
    }
    for (ll &x : c) {
        cin >> x; // c1,c2,...,ck in this order
        x = norm(x);
    }
    Mat x(k);
    for (int i = 0; i + 1 < k; i++) x.a[i][i + 1] = 1;
    for (int j = 0; j < k; j++) x.a[k - 1][j] = c[k - 1 - j];
    Mat b = power(x, n);
    for (int i = 0; i < k; i++) {
        ll ans = 0;
        for (int j = 0; j < k; j++) ans = (ans + b.a[i][j] * f[j]) % MOD;
        cout << ans << ' ';
    }
    cout << "\n";
}

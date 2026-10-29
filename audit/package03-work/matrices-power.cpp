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
    int n;
    ll k;
    cin >> n >> k; // 1 <= n <= 80; 0 <= k <= 10^18
    Mat a(n);
    for (auto &row : a.a) for (ll &x : row) {
        cin >> x;
        x = norm(x);
    }
    Mat b = power(a, k);
    for (auto &row : b.a) {
        for (ll x : row) cout << x << ' ';
        cout << "\n";
    }
}

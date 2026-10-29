#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Mat {
    int n;
    vector<vector<long double>> a;
    Mat(int _n, bool id = false) : n(_n), a(n, vector<long double>(n)) {
        if (id) for (int i = 0; i < n; i++) a[i][i] = 1;
    }
    Mat operator*(const Mat &b) const {
        Mat c(n);
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                for (int j = 0; j < n; j++) c.a[i][j] += a[i][k] * b.a[k][j];
            }
        }
        for (int j = 0; j < n; j++) {
            long double sum = 0;
            for (int i = 0; i < n; i++) sum += c.a[i][j];
            for (int i = 0; i < n; i++) c.a[i][j] /= sum;
        }
        return c;
    }
};

Mat power(Mat a, ll k) {
    Mat ans(a.n, true);
    while (k) {
        if (k & 1) ans = ans * a;
        a = a * a;
        k >>= 1;
    }
    return ans;
}

int main() {
    int n;
    ll k;
    cin >> n >> k;
    Mat p(n);
    if (n == 1) p.a[0][0] = 1;
    else {
        for (int j = 0; j < n; j++) {
            if (j == 0) p.a[1][j] = 1;
            else if (j == n - 1) p.a[n - 2][j] = 1;
            else p.a[j - 1][j] = p.a[j + 1][j] = 0.5L;
        }
    }
    auto ans = power(p, k);
    cout << fixed << setprecision(18);
    for (int i = 0; i < n; i++) cout << ans.a[i][0] << ' ';
    cout << '\n';
}

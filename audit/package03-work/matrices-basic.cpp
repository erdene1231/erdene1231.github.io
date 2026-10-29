#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Mat {
    int r, c;
    vector<vector<ll>> a;

    Mat(int _r, int _c) {
        r = _r;
        c = _c;
        a.assign(r, vector<ll>(c));
    }

    Mat transpose() const {
        Mat b(c, r);
        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) b.a[j][i] = a[i][j];
        }
        return b;
    }

    Mat operator+(const Mat &b) const {
        Mat res(r, c);
        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) res.a[i][j] = a[i][j] + b.a[i][j];
        }
        return res;
    }

    Mat scale(ll x) const {
        Mat res(r, c);
        for (int i = 0; i < r; i++) {
            for (int j = 0; j < c; j++) res.a[i][j] = x * a[i][j];
        }
        return res;
    }

    Mat operator*(const Mat &b) const {
        Mat res(r, b.c);
        for (int i = 0; i < r; i++) {
            for (int k = 0; k < c; k++) {
                for (int j = 0; j < b.c; j++) res.a[i][j] += a[i][k] * b.a[k][j];
            }
        }
        return res;
    }
};

void read(Mat &a) {
    for (auto &row : a.a) for (ll &x : row) cin >> x;
}

void print(const Mat &a) {
    cout << a.r << ' ' << a.c << "\n";
    for (const auto &row : a.a) {
        for (ll x : row) cout << x << ' ';
        cout << "\n";
    }
}

int main() {
    int r, n, c;
    ll x;
    cin >> r >> n >> c >> x; // dimensions 1..30; |x|,|entries| <= 10^6
    Mat a(r, n), b(n, c), d(r, n);
    read(a);
    read(b);
    read(d);
    print(a + d);
    print(a.scale(x));
    print(a.transpose());
    print(a * b);
}

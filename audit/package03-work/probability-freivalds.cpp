#include <bits/stdc++.h>
using namespace std;
using ll = long long;

using Mat = vector<vector<ll>>;

vector<ll> mul(const Mat &a, const vector<ll> &x) {
    int n = (int)a.size();
    vector<ll> y(n);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) y[i] += a[i][j] * x[j];
    }
    return y;
}

int main() {
    int n, t;
    unsigned long long seed;
    cin >> n >> t >> seed;
    Mat a(n, vector<ll>(n)), b = a, c = a;
    for (auto *p : {&a, &b, &c}) {
        for (auto &row : *p) for (auto &v : row) cin >> v;
    }
    mt19937_64 rng(seed);
    for (int round = 0; round < t; round++) {
        vector<ll> x(n);
        for (auto &v : x) v = uniform_int_distribution<int>(0, 1)(rng);
        if (mul(a, mul(b, x)) != mul(c, x)) {
            cout << "DIFFERENT\n";
            for (auto v : x) cout << v << ' ';
            cout << '\n';
            return 0;
        }
    }
    cout << "PROBABLY EQUAL\n";
}

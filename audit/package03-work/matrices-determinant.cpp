#include <bits/stdc++.h>
using namespace std;
using ll = long long;

using Matrix = vector<vector<ll>>;

Matrix minorOf(const Matrix &a, int r, int c) {
    int n = a.size();
    Matrix b;
    for (int i = 0; i < n; i++) {
        if (i == r) continue;
        vector<ll> row;
        for (int j = 0; j < n; j++) if (j != c) row.push_back(a[i][j]);
        b.push_back(row);
    }
    return b;
}

ll det(const Matrix &a) {
    int n = a.size();
    if (n == 0) return 1;
    if (n == 1) return a[0][0];
    ll res = 0;
    for (int j = 0; j < n; j++) {
        ll term = a[0][j] * det(minorOf(a, 0, j));
        res += (j % 2 ? -term : term);
    }
    return res;
}

int main() {
    int n;
    cin >> n; // 1 <= n <= 6; |entries| <= 20
    Matrix a(n, vector<ll>(n));
    for (auto &row : a) for (ll &x : row) cin >> x;
    ll d = det(a);
    cout << d << "\n";
    if (d == 0) {
        cout << "SINGULAR\n";
        return 0;
    }
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            ll x = det(minorOf(a, j, i)); // transposed cofactor
            if ((i + j) % 2) x = -x;
            ll y = d, g = gcd(abs(x), abs(y));
            x /= g;
            y /= g;
            if (y < 0) x = -x, y = -y;
            cout << x << '/' << y << ' ';
        }
        cout << "\n";
    }
}

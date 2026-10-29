#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll INF = 4000000000000000000LL;

struct Mat {
    int n;
    vector<vector<ll>> a;

    Mat(int _n, bool unit = false) {
        n = _n;
        a.assign(n, vector<ll>(n, INF));
        if (unit) for (int i = 0; i < n; i++) a[i][i] = 0;
    }

    Mat operator*(const Mat &b) const {
        Mat res(n);
        for (int i = 0; i < n; i++) {
            for (int k = 0; k < n; k++) {
                if (a[i][k] == INF) continue;
                for (int j = 0; j < n; j++) {
                    if (b.a[k][j] == INF) continue;
                    res.a[i][j] = min(res.a[i][j], a[i][k] + b.a[k][j]);
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
    int n, m;
    ll k;
    cin >> n >> m >> k; // 1 <= n <= 80; m <= 10000; 0 <= k <= 10^12
    Mat a(n);
    for (int i = 0; i < m; i++) {
        int u, v;
        ll w;
        cin >> u >> v >> w; // |w| <= 10^6
        --u;
        --v;
        a.a[u][v] = min(a.a[u][v], w);
    }
    Mat b = power(a, k);
    for (auto &row : b.a) {
        for (ll x : row) {
            if (x == INF) cout << "INF ";
            else cout << x << ' ';
        }
        cout << "\n";
    }
}

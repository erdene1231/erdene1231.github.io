#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Prefix2D {
    int n, m;
    vector<vector<ll>> p;

    Prefix2D(int _n, int _m) {
        n = _n;
        m = _m;
        p.assign(n + 1, vector<ll>(m + 1));
    }

    void build(const vector<vector<ll>> &a) {
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                p[i + 1][j + 1] = a[i][j] + p[i][j + 1] + p[i + 1][j] - p[i][j];
            }
        }
    }

    ll sum(int y1, int x1, int y2, int x2) const {
        return p[y2][x2] - p[y1][x2] - p[y2][x1] + p[y1][x1];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    vector<vector<ll>> a(n, vector<ll>(m));
    for (auto &row : a) {
        for (ll &x : row) cin >> x;
    }
    Prefix2D pref(n, m);
    pref.build(a);
    while (q--) {
        int y1, x1, y2, x2;
        cin >> y1 >> x1 >> y2 >> x2;
        cout << pref.sum(y1 - 1, x1 - 1, y2, x2) << '\n';
    }
    return 0;
}

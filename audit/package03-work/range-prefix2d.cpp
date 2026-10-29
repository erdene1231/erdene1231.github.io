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
    void build(const vector<vector<int>>& a) {
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                p[i][j] = a[i - 1][j - 1] + p[i - 1][j] + p[i][j - 1] - p[i - 1][j - 1];
            }
        }
    }
    ll sum(int x1, int y1, int x2, int y2) const {
        return p[x2][y2] - p[x1 - 1][y2] - p[x2][y1 - 1] + p[x1 - 1][y1 - 1];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, q;
    cin >> n >> m >> q;
    vector<vector<int>> a(n, vector<int>(m));
    for (auto& row : a) for (int& x : row) cin >> x;
    Prefix2D pref(n, m);
    pref.build(a);
    while (q--) {
        int x1, y1, x2, y2;
        cin >> x1 >> y1 >> x2 >> y2;
        cout << pref.sum(x1, y1, x2, y2) << '\n';
    }
}

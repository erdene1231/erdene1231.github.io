#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h, w;
    cin >> h >> w;
    vector<vector<ll>> a(h, vector<ll>(w)), b = a;
    for (auto &row : a) for (ll &x : row) cin >> x;
    for (auto &row : b) for (ll &x : row) cin >> x;
    ll moves = 0;
    for (int i = 0; i + 1 < h; ++i) {
        for (int j = 0; j + 1 < w; ++j) {
            ll delta = b[i][j] - a[i][j];
            for (int di = 0; di < 2; ++di) {
                for (int dj = 0; dj < 2; ++dj) a[i + di][j + dj] += delta;
            }
            moves += abs(delta);
        }
    }
    if (a != b) cout << "No\n";
    else cout << "Yes\n" << moves << '\n';
}

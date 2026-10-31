#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    const int limit = 1000;
    vector<vector<int>> d(limit + 1, vector<int>(limit + 1));
    for (int i = 0; i < n; ++i) {
        int lx, ly, rx, ry;
        cin >> lx >> ly >> rx >> ry;
        ++d[lx][ly];
        --d[rx][ly];
        --d[lx][ry];
        ++d[rx][ry];
    }
    for (int x = 0; x <= limit; ++x) {
        for (int y = 1; y <= limit; ++y) d[x][y] += d[x][y - 1];
    }
    for (int x = 1; x <= limit; ++x) {
        for (int y = 0; y <= limit; ++y) d[x][y] += d[x - 1][y];
    }
    vector<int> area(n + 1);
    for (int x = 0; x < limit; ++x) {
        for (int y = 0; y < limit; ++y) ++area[d[x][y]];
    }
    for (int k = 1; k <= n; ++k) cout << area[k] << '\n';
}

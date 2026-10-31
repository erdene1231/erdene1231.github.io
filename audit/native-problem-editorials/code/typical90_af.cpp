#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<int>> a(n, vector<int>(n));
    for (auto &row : a) for (int &x : row) cin >> x;
    int m;
    cin >> m;
    vector<vector<char>> bad(n, vector<char>(n));
    while (m--) {
        int x, y;
        cin >> x >> y;
        --x;
        --y;
        bad[x][y] = bad[y][x] = true;
    }
    vector<int> p(n);
    iota(p.begin(), p.end(), 0);
    const int inf = 1000000000;
    int ans = inf;
    do {
        bool ok = true;
        for (int j = 1; j < n; ++j) {
            if (bad[p[j - 1]][p[j]]) ok = false;
        }
        if (!ok) continue;
        int sum = 0;
        for (int j = 0; j < n; ++j) sum += a[p[j]][j];
        ans = min(ans, sum);
    } while (next_permutation(p.begin(), p.end()));
    cout << (ans == inf ? -1 : ans) << '\n';
}

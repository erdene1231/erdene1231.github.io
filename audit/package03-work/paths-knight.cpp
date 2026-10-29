#include <bits/stdc++.h>
using namespace std;

struct Knight {
    int n;
    vector<vector<int>> a;
    const vector<pair<int, int>> moves = {
        {-2, -1}, {-2, 1}, {-1, -2}, {-1, 2},
        {1, -2}, {1, 2}, {2, -1}, {2, 1}
    };
    Knight(int _n) {
        n = _n;
        a.assign(n, vector<int>(n));
    }
    bool free(int x, int y) const {
        return 0 <= x && x < n && 0 <= y && y < n && a[x][y] == 0;
    }
    int degree(int x, int y) const {
        int ans = 0;
        for (auto [dx, dy] : moves) ans += free(x + dx, y + dy);
        return ans;
    }
    bool dfs(int x, int y, int step) {
        a[x][y] = step;
        if (step == n * n) return true;
        vector<array<int, 3>> next;
        for (auto [dx, dy] : moves) {
            int u = x + dx, v = y + dy;
            if (free(u, v)) next.push_back({degree(u, v), u, v});
        }
        sort(next.begin(), next.end());
        for (auto [d, u, v] : next) if (dfs(u, v, step + 1)) return true;
        a[x][y] = 0;
        return false;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, x, y;
    cin >> n >> x >> y;
    Knight g(n);
    if (!g.dfs(x - 1, y - 1, 1)) cout << "IMPOSSIBLE\n";
    else for (const auto &row : g.a) {
        for (int step : row) cout << step << ' ';
        cout << '\n';
    }
}

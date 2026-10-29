#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Maze {
    int n, m;
    vector<string> a;
    vector<vector<int>> g;
    Maze(vector<string> _a) : n((int)_a.size()), m((int)_a[0].size()), a(_a), g(n, vector<int>(m, -1)) {
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < m; c++) {
                if (a[r][c] == '#') continue;
                int d = r + c;
                vector<bool> seen(d + 1);
                for (int i = r - 1; i >= 0 && a[i][c] != '#'; i--) {
                    if (g[i][c] <= d) seen[g[i][c]] = true;
                }
                for (int j = c - 1; j >= 0 && a[r][j] != '#'; j--) {
                    if (g[r][j] <= d) seen[g[r][j]] = true;
                }
                g[r][c] = 0;
                while (g[r][c] <= d && seen[g[r][c]]) g[r][c]++;
            }
        }
    }
    pair<int, int> move(int r, int c, int target) const {
        for (int i = r - 1; i >= 0 && a[i][c] != '#'; i--) {
            if (g[i][c] == target) return {i, c};
        }
        for (int j = c - 1; j >= 0 && a[r][j] != '#'; j--) {
            if (g[r][j] == target) return {r, j};
        }
        return {-1, -1};
    }
};

int main() {
    int t;
    cin >> t;
    vector<Maze> mazes;
    vector<pair<int, int>> pos;
    int s = 0;
    for (int i = 0; i < t; i++) {
        int n, m, r, c;
        cin >> n >> m;
        vector<string> a(n);
        for (auto &row : a) cin >> row;
        cin >> r >> c;
        mazes.emplace_back(a);
        pos.push_back({r - 1, c - 1});
        s ^= mazes.back().g[r - 1][c - 1];
    }
    for (int i = 0; i < t; i++) {
        auto [r, c] = pos[i];
        cout << mazes[i].g[r][c] << ' ';
    }
    cout << '\n';
    if (s == 0) cout << "LOSE\n";
    else {
        for (int i = 0; i < t; i++) {
            auto [r, c] = pos[i];
            int x = mazes[i].g[r][c], target = x ^ s;
            if (target >= x) continue;
            auto [nr, nc] = mazes[i].move(r, c, target);
            cout << "WIN " << i + 1 << ' ' << nr + 1 << ' ' << nc + 1 << '\n';
            break;
        }
    }
    for (const auto &maze : mazes) {
        for (const auto &row : maze.g) {
            for (int x : row) cout << x << ' ';
            cout << '\n';
        }
    }
}

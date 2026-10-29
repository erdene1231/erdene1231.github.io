#include <bits/stdc++.h>
using namespace std;

int n, level;
bool used[9][9];
int dr[] = {1, 0, -1, 0};
int dc[] = {0, 1, 0, -1};

int search(int r, int c, int length) {
    if (length == n * n) return r == n && c == n;
    if (level >= 2 && r == n && c == n) return 0;
    bool split = (used[r - 1][c] && used[r + 1][c] &&
                  !used[r][c - 1] && !used[r][c + 1]) ||
                 (used[r][c - 1] && used[r][c + 1] &&
                  !used[r - 1][c] && !used[r + 1][c]);
    bool wall = r == 1 || r == n || c == 1 || c == n;
    if ((level >= 4 || (level >= 3 && wall)) && split) return 0;
    int ans = 0;
    for (int d = 0; d < 4; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (used[nr][nc]) continue;
        used[nr][nc] = true;
        ans += search(nr, nc, length + 1);
        used[nr][nc] = false;
    }
    return ans;
}

int count_paths(int size, int optimization) {
    n = size;
    level = optimization;
    for (auto& row : used) fill(begin(row), end(row), true);
    for (int r = 1; r <= n; r++) {
        for (int c = 1; c <= n; c++) used[r][c] = false;
    }
    used[1][1] = true;
    if (n == 1) return 1;
    if (level >= 1) {
        used[2][1] = true;
        return 2 * search(2, 1, 2);
    }
    return search(1, 1, 1);
}

int main() {
    int size, optimization;
    cin >> size >> optimization; // 1 <= size <= 7, 0 <= optimization <= 4.
    cout << count_paths(size, optimization) << "\n";
    return 0;
}

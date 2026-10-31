#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h, w;
    cin >> h >> w;
    vector<string> grid(h);
    for (string &row : grid) cin >> row;
    vector<vector<int>> adj(h * w);
    int dr[] = {-1, 1, 0, 0}, dc[] = {0, 0, -1, 1};
    for (int r = 0; r < h; ++r) {
        for (int c = 0; c < w; ++c) {
            if (grid[r][c] == '#') continue;
            for (int d = 0; d < 4; ++d) {
                int nr = r + dr[d], nc = c + dc[d];
                if (nr >= 0 && nr < h && nc >= 0 && nc < w && grid[nr][nc] == '.') {
                    adj[r * w + c].push_back(nr * w + nc);
                }
            }
        }
    }
    int ans = -1;
    for (int start = 0; start < h * w; ++start) {
        auto dfs = [&](auto &&self, int at, int used, int length) -> void {
            for (int next : adj[at]) {
                if (next == start) {
                    if (length >= 3) ans = max(ans, length);
                } else if (next > start && !(used >> next & 1)) {
                    self(self, next, used | (1 << next), length + 1);
                }
            }
        };
        dfs(dfs, start, 1 << start, 1);
    }
    cout << ans << '\n';
}

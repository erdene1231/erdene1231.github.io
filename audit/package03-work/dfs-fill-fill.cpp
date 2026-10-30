#include <bits/stdc++.h>
using namespace std;

struct Grid {
    int n, m;
    vector<string> a;
    vector<vector<int>> id;
    vector<pair<int, int>> stats;

    Grid(int _n, int _m) {
        n = _n;
        m = _m;
        a.resize(n);
        id.assign(n, vector<int>(m, -1));
    }

    void fill(int sy, int sx) {
        const int dy[4] = {-1, 1, 0, 0};
        const int dx[4] = {0, 0, -1, 1};
        int c = stats.size();
        int area = 0, per = 0;
        vector<pair<int, int>> st;
        id[sy][sx] = c;
        st.push_back({sy, sx});
        while (!st.empty()) {
            auto [y, x] = st.back();
            st.pop_back();
            area++;
            for (int d = 0; d < 4; d++) {
                int ny = y + dy[d], nx = x + dx[d];
                if (ny < 0 || ny >= n || nx < 0 || nx >= m || a[ny][nx] == '#') {
                    per++;
                    continue;
                }
                if (id[ny][nx] == -1) {
                    id[ny][nx] = c;
                    st.push_back({ny, nx});
                }
            }
        }
        stats.push_back({area, per});
    }

    void run() {
        for (int y = 0; y < n; y++) {
            for (int x = 0; x < m; x++) {
                if (a[y][x] == '.' && id[y][x] == -1) fill(y, x);
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    Grid grid(n, m);
    if (m > 0) {
        for (string &row : grid.a) cin >> row;
    }
    grid.run();
    cout << grid.stats.size() << '\n';
    for (auto [area, per] : grid.stats) cout << area << ' ' << per << '\n';
    return 0;
}

#include <bits/stdc++.h>
using namespace std;

struct DSU {
    vector<int> p;
    explicit DSU(int n) : p(n, -1) {}
    int root(int x) {
        return p[x] < 0 ? x : p[x] = root(p[x]);
    }
    void join(int a, int b) {
        a = root(a);
        b = root(b);
        if (a == b) return;
        if (p[a] > p[b]) swap(a, b);
        p[a] += p[b];
        p[b] = a;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h, w, q;
    cin >> h >> w >> q;
    DSU dsu(h * w);
    vector<char> red(h * w);
    const int dr[] = {-1, 1, 0, 0};
    const int dc[] = {0, 0, -1, 1};
    while (q--) {
        int type, r, c;
        cin >> type >> r >> c;
        --r;
        --c;
        int u = r * w + c;
        if (type == 1) {
            red[u] = true;
            for (int dir = 0; dir < 4; ++dir) {
                int nr = r + dr[dir], nc = c + dc[dir];
                if (nr < 0 || nr >= h || nc < 0 || nc >= w) continue;
                int v = nr * w + nc;
                if (red[v]) dsu.join(u, v);
            }
        } else {
            int nr, nc;
            cin >> nr >> nc;
            int v = (nr - 1) * w + nc - 1;
            bool ok = red[u] && red[v] && dsu.root(u) == dsu.root(v);
            cout << (ok ? "Yes" : "No") << '\n';
        }
    }
}

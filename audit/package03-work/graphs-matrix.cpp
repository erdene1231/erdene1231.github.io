#include <bits/stdc++.h>
using namespace std;

struct Matrix {
    int n;
    bool dir;
    vector<vector<int>> adj;
    Matrix(int _n, bool _dir) {
        n = _n;
        dir = _dir;
        adj.assign(n + 1, vector<int>(n + 1));
    }
    void add(int a, int b) {
        adj[a][b] = 1;
        if (!dir) adj[b][a] = 1;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir;
    cin >> n >> m >> dir;
    Matrix g(n, dir);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    for (int a = 1; a <= n; a++) {
        for (int b = 1; b <= n; b++) cout << g.adj[a][b] << (b == n ? '\n' : ' ');
    }
}

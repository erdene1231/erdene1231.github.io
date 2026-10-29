#include <bits/stdc++.h>
using namespace std;

using ll = long long;

struct Matrix {
    int n;
    bool dir;
    vector<vector<char>> has;
    vector<vector<ll>> weight;
    Matrix(int _n, bool _dir) {
        n = _n;
        dir = _dir;
        has.assign(n + 1, vector<char>(n + 1));
        weight.assign(n + 1, vector<ll>(n + 1));
    }
    void put(int a, int b, ll w) {
        if (!has[a][b] || w < weight[a][b]) weight[a][b] = w;
        has[a][b] = 1;
    }
    void add(int a, int b, ll w) {
        put(a, b, w);
        if (!dir) put(b, a, w);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir;
    cin >> n >> m >> dir;
    Matrix g(n, dir);
    for (int i = 0; i < m; i++) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        g.add(a, b, w);
    }
    for (int a = 1; a <= n; a++) {
        for (int b = 1; b <= n; b++) {
            if (b > 1) cout << ' ';
            if (g.has[a][b]) cout << g.weight[a][b];
            else cout << '.';
        }
        cout << '\n';
    }
}

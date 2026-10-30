#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll INF = 1LL << 60;

struct Floyd {
    int n;
    vector<vector<ll>> d;

    Floyd(int _n) {
        n = _n;
        d.assign(n + 1, vector<ll>(n + 1, INF));
        for (int i = 1; i <= n; i++) d[i][i] = 0;
    }

    void add(int a, int b, ll w) {
        d[a][b] = min(d[a][b], w);
        d[b][a] = min(d[b][a], w);
    }

    void run() {
        for (int k = 1; k <= n; k++) {
            for (int i = 1; i <= n; i++) {
                if (d[i][k] == INF) continue;
                for (int j = 1; j <= n; j++) {
                    if (d[k][j] == INF) continue;
                    d[i][j] = min(d[i][j], d[i][k] + d[k][j]);
                }
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m, q;
    cin >> n >> m >> q;
    Floyd fw(n);
    while (m--) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        fw.add(a, b, w);
    }
    fw.run();
    while (q--) {
        int a, b;
        cin >> a >> b;
        cout << (fw.d[a][b] == INF ? -1 : fw.d[a][b]) << '\n';
    }
    return 0;
}

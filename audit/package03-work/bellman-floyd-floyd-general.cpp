#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const ll INF = 1LL << 60;

struct Floyd {
    int n;
    vector<vector<ll>> d;
    vector<vector<int>> nxt, bad;

    Floyd(int _n) {
        n = _n;
        d.assign(n + 1, vector<ll>(n + 1, INF));
        nxt.assign(n + 1, vector<int>(n + 1, -1));
        bad.assign(n + 1, vector<int>(n + 1));
        for (int i = 1; i <= n; i++) {
            d[i][i] = 0;
            nxt[i][i] = i;
        }
    }

    void add(int a, int b, ll w) {
        if (w < d[a][b]) {
            d[a][b] = w;
            nxt[a][b] = b;
        }
    }

    void run() {
        for (int k = 1; k <= n; k++) {
            for (int i = 1; i <= n; i++) {
                if (d[i][k] == INF) continue;
                for (int j = 1; j <= n; j++) {
                    if (d[k][j] == INF) continue;
                    ll nd = max(-INF, d[i][k] + d[k][j]);
                    if (nd < d[i][j]) {
                        d[i][j] = nd;
                        nxt[i][j] = nxt[i][k];
                    }
                }
            }
        }
        for (int k = 1; k <= n; k++) {
            if (d[k][k] >= 0) continue;
            for (int i = 1; i <= n; i++) {
                if (d[i][k] == INF) continue;
                for (int j = 1; j <= n; j++) {
                    if (d[k][j] != INF) bad[i][j] = 1;
                }
            }
        }
    }

    vector<int> path(int a, int b) const {
        if (d[a][b] == INF || bad[a][b]) return {};
        vector<int> p = {a};
        while (a != b) {
            a = nxt[a][b];
            p.push_back(a);
        }
        return p;
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
        if (fw.bad[a][b]) cout << "-INF\n";
        else if (fw.d[a][b] == INF) cout << "UNREACHABLE\n";
        else {
            auto p = fw.path(a, b);
            cout << fw.d[a][b] << ' ' << p.size();
            for (int v : p) cout << ' ' << v;
            cout << '\n';
        }
    }
    return 0;
}

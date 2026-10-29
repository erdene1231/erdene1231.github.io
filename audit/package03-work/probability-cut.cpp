#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    int n, m;
    unsigned long long seed;
    cin >> n >> m >> seed;
    vector<pair<int, int>> edges(m);
    for (auto &[u, v] : edges) {
        cin >> u >> v;
        u--;
        v--;
    }
    mt19937_64 rng(seed);
    vector<int> col(n);
    ll trials = 0;
    while (true) {
        trials++;
        for (auto &c : col) c = uniform_int_distribution<int>(0, 1)(rng);
        int cut = 0;
        for (auto [u, v] : edges) cut += col[u] != col[v];
        if (2 * cut >= m) {
            cout << cut << ' ' << trials << '\n';
            for (auto c : col) cout << c << ' ';
            cout << '\n';
            return 0;
        }
    }
}

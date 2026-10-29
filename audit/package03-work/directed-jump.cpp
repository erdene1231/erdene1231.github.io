#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Jump {
    static const int L = 60;
    vector<array<int, L>> up;
    Jump(const vector<int> &succ) {
        int n = (int)succ.size() - 1;
        up.resize(n + 1);
        for (int u = 1; u <= n; u++) up[u][0] = succ[u];
        for (int j = 1; j < L; j++) {
            for (int u = 1; u <= n; u++) up[u][j] = up[up[u][j - 1]][j - 1];
        }
    }
    int get(int u, ll k) const {
        for (int j = 0; j < L; j++) {
            if ((k >> j) & 1LL) u = up[u][j];
        }
        return u;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> succ(n + 1);
    for (int u = 1; u <= n; u++) cin >> succ[u];
    Jump g(succ);
    while (q--) {
        int u;
        ll k;
        cin >> u >> k;
        cout << g.get(u, k) << '\n';
    }
}

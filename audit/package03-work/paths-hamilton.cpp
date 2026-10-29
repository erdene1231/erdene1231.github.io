#include <bits/stdc++.h>
using namespace std;

struct HamiltonDP {
    int n;
    vector<unsigned> adj, in;
    HamiltonDP(int _n) {
        n = _n;
        adj.resize(n);
        in.resize(n);
    }
    void add(int a, int b) {
        adj[a] |= 1U << b;
        in[b] |= 1U << a;
    }
    vector<int> solve(bool closed) const {
        if (closed && n < 3) return {};
        unsigned full = (1U << n) - 1;
        vector<unsigned> dp(1U << n);
        for (int u = 0; u < (closed ? 1 : n); u++) dp[1U << u] = 1U << u;
        for (unsigned mask = 1; mask <= full; mask++) {
            unsigned ends = dp[mask];
            while (ends) {
                int u = __builtin_ctz(ends);
                ends &= ends - 1;
                unsigned next = adj[u] & (full ^ mask);
                while (next) {
                    int v = __builtin_ctz(next);
                    next &= next - 1;
                    dp[mask | (1U << v)] |= 1U << v;
                }
            }
        }
        unsigned ends = dp[full];
        if (closed) ends &= in[0];
        if (!ends) return {};
        int u = __builtin_ctz(ends);
        unsigned mask = full;
        vector<int> path;
        while (true) {
            path.push_back(u);
            mask ^= 1U << u;
            if (!mask) break;
            unsigned prev = dp[mask] & in[u];
            u = __builtin_ctz(prev);
        }
        reverse(path.begin(), path.end());
        if (closed) path.push_back(0);
        return path;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, directed, closed;
    cin >> n >> m >> directed >> closed;
    HamiltonDP g(n);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.add(--a, --b);
        if (!directed) g.add(b, a);
    }
    auto ans = g.solve(closed);
    if (ans.empty()) cout << "IMPOSSIBLE\n";
    else {
        for (int u : ans) cout << u + 1 << ' ';
        cout << '\n';
    }
}

#include <bits/stdc++.h>
using namespace std;

struct Euler {
    int n, m = 0;
    bool directed;
    vector<vector<pair<int, int>>> adj;
    vector<int> in, out;
    Euler(int _n, bool _directed) {
        n = _n;
        directed = _directed;
        adj.resize(n);
        in.resize(n);
        out.resize(n);
    }
    void add(int a, int b) {
        adj[a].push_back({b, m});
        out[a]++;
        in[b]++;
        if (!directed) {
            adj[b].push_back({a, m});
            out[b]++;
            in[a]++;
        }
        m++;
    }
    vector<int> trail() const {
        int start = 0, odd = 0, plus = 0, minus = 0;
        for (int u = 0; u < n; u++) if (out[u]) start = u;
        for (int u = 0; u < n; u++) {
            if (!directed) {
                if (out[u] % 2) {
                    odd++;
                    start = u;
                }
            } else {
                int d = out[u] - in[u];
                if (abs(d) > 1) return {};
                if (d == 1) plus++, start = u;
                if (d == -1) minus++;
            }
        }
        if (!directed && odd != 0 && odd != 2) return {};
        if (directed && !((plus == 0 && minus == 0) || (plus == 1 && minus == 1))) return {};
        vector<int> ptr(n), used(m), st = {start}, ans;
        while (!st.empty()) {
            int u = st.back();
            while (ptr[u] < (int)adj[u].size() && used[adj[u][ptr[u]].second]) ptr[u]++;
            if (ptr[u] == (int)adj[u].size()) {
                ans.push_back(u);
                st.pop_back();
            } else {
                auto [v, id] = adj[u][ptr[u]++];
                used[id] = true;
                st.push_back(v);
            }
        }
        if ((int)ans.size() != m + 1) return {};
        reverse(ans.begin(), ans.end());
        return ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, directed;
    cin >> n >> m >> directed;
    Euler g(n, directed);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.add(a - 1, b - 1);
    }
    auto ans = g.trail();
    if (ans.empty()) cout << "IMPOSSIBLE\n";
    else {
        for (int u : ans) cout << u + 1 << ' ';
        cout << '\n';
    }
}

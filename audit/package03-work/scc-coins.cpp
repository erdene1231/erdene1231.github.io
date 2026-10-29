#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct SCC {
    int n;
    vector<vector<int>> g, rg, groups;
    vector<int> comp, ord, tin, tout;
    SCC(int _n) {
        n = _n;
        g.resize(n);
        rg.resize(n);
    }
    void add(int a, int b) {
        g[a].push_back(b);
        rg[b].push_back(a);
    }
    int run() {
        vector<int> seen(n);
        comp.assign(n, -1);
        tin.assign(n, 0);
        tout.assign(n, 0);
        ord.clear();
        groups.clear();
        int timer = 0;
        for (int s = 0; s < n; s++) {
            if (seen[s]) continue;
            vector<pair<int, int>> st = {{s, 0}};
            seen[s] = true;
            tin[s] = ++timer;
            while (!st.empty()) {
                int u = st.back().first;
                int &i = st.back().second;
                if (i == (int)g[u].size()) {
                    tout[u] = ++timer;
                    ord.push_back(u);
                    st.pop_back();
                    continue;
                }
                int v = g[u][i++];
                if (!seen[v]) {
                    seen[v] = true;
                    tin[v] = ++timer;
                    st.push_back({v, 0});
                }
            }
        }
        for (int i = n - 1; i >= 0; i--) {
            int s = ord[i];
            if (comp[s] != -1) continue;
            int c = (int)groups.size();
            groups.push_back({});
            vector<int> st = {s};
            comp[s] = c;
            while (!st.empty()) {
                int u = st.back();
                st.pop_back();
                groups[c].push_back(u);
                for (int v : rg[u]) {
                    if (comp[v] != -1) continue;
                    comp[v] = c;
                    st.push_back(v);
                }
            }
        }
        return (int)groups.size();
    }
    vector<vector<int>> dag() const {
        int k = (int)groups.size();
        vector<vector<int>> adj(k);
        vector<int> seen(k, -1);
        for (int c = 0; c < k; c++) {
            for (int u : groups[c]) {
                for (int v : g[u]) {
                    int d = comp[v];
                    if (c == d || seen[d] == c) continue;
                    seen[d] = c;
                    adj[c].push_back(d);
                }
            }
        }
        return adj;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<ll> coins(n);
    for (ll &x : coins) cin >> x;
    SCC s(n);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        s.add(a - 1, b - 1);
    }
    int k = s.run();
    auto adj = s.dag();
    vector<ll> sum(k), best(k);
    for (int u = 0; u < n; u++) sum[s.comp[u]] += coins[u];
    best = sum;
    for (int c = 0; c < k; c++) {
        for (int d : adj[c]) best[d] = max(best[d], best[c] + sum[d]);
    }
    cout << *max_element(best.begin(), best.end()) << '\n';
}

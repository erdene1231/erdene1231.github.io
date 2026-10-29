#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct TreeOrder {
    int n;
    vector<vector<int>> adj;
    vector<int> par, tin, sz, ord;
    TreeOrder(int _n) {
        n = _n;
        adj.resize(n + 1);
        par.resize(n + 1);
        tin.resize(n + 1);
        sz.assign(n + 1, 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    void build(int root) {
        vector<int> st = {root};
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            tin[u] = (int)ord.size() + 1;
            ord.push_back(u);
            for (int i = (int)adj[u].size() - 1; i >= 0; i--) {
                int v = adj[u][i];
                if (v == par[u]) continue;
                par[v] = u;
                st.push_back(v);
            }
        }
        for (int i = n - 1; i > 0; i--) sz[par[ord[i]]] += sz[ord[i]];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, root;
    cin >> n >> q >> root;
    vector<int> val(n + 1);
    for (int u = 1; u <= n; u++) cin >> val[u];
    TreeOrder g(n);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.build(root);
    vector<vector<pair<int, int>>> queries(n + 1);
    for (int i = 0, u, x; i < q; i++) {
        cin >> u >> x;
        queries[u].push_back({x, i});
    }
    vector<map<int, int>> bag(n + 1);
    vector<int> ans(q);
    for (int i = n - 1; i >= 0; i--) {
        int u = g.ord[i];
        bag[u][val[u]]++;
        for (int v : g.adj[u]) {
            if (g.par[v] != u) continue;
            if (bag[u].size() < bag[v].size()) bag[u].swap(bag[v]);
            for (auto [x, cnt] : bag[v]) bag[u][x] += cnt;
            bag[v].clear();
        }
        for (auto [x, id] : queries[u]) {
            auto it = bag[u].find(x);
            ans[id] = it == bag[u].end() ? 0 : it->second;
        }
    }
    for (int x : ans) cout << x << '\n';
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct EulerLCA {
    int n;
    vector<vector<int>> adj, st;
    vector<int> dep, first, tour, lg;
    EulerLCA(int _n) {
        n = _n;
        adj.resize(n + 1);
        dep.resize(n + 1);
        first.assign(n + 1, -1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }
    void build(int root) {
        vector<array<int, 3>> stack = {{root, 0, 0}};
        first[root] = 0;
        tour.push_back(root);
        while (!stack.empty()) {
            int u = stack.back()[0], p = stack.back()[1];
            int &i = stack.back()[2];
            if (i == (int)adj[u].size()) {
                stack.pop_back();
                if (!stack.empty()) tour.push_back(stack.back()[0]);
                continue;
            }
            int v = adj[u][i++];
            if (v == p) continue;
            dep[v] = dep[u] + 1;
            first[v] = (int)tour.size();
            tour.push_back(v);
            stack.push_back({v, u, 0});
        }
        int m = (int)tour.size();
        lg.assign(m + 1, 0);
        for (int i = 2; i <= m; i++) lg[i] = lg[i / 2] + 1;
        st.assign(lg[m] + 1, vector<int>(m));
        st[0] = tour;
        for (int j = 1; j <= lg[m]; j++) {
            for (int i = 0; i + (1 << j) <= m; i++) {
                int a = st[j - 1][i], b = st[j - 1][i + (1 << (j - 1))];
                st[j][i] = dep[a] <= dep[b] ? a : b;
            }
        }
    }
    int lca(int a, int b) const {
        int l = first[a], r = first[b];
        if (l > r) swap(l, r);
        int k = lg[r - l + 1];
        a = st[k][l];
        b = st[k][r - (1 << k) + 1];
        return dep[a] <= dep[b] ? a : b;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q, root;
    cin >> n >> q >> root;
    EulerLCA g(n);
    for (int i = 1, a, b; i < n; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.build(root);
    while (q--) {
        int a, b;
        cin >> a >> b;
        int c = g.lca(a, b);
        cout << c << ' ' << g.dep[a] + g.dep[b] - 2 * g.dep[c] << '\n';
    }
}

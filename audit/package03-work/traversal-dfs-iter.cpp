#include <bits/stdc++.h>
using namespace std;

struct Graph {
    int n;
    bool dir;
    vector<vector<int>> adj;
    vector<int> vis, ord;
    Graph(int _n, bool _dir) {
        n = _n;
        dir = _dir;
        adj.resize(n + 1);
        vis.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back(b);
        if (!dir) adj[b].push_back(a);
    }
    void dfs(int s) {
        vector<int> it(n + 1), st = {s};
        vis[s] = 1;
        ord.push_back(s);
        while (!st.empty()) {
            int u = st.back();
            if (it[u] == (int)adj[u].size()) {
                st.pop_back();
                continue;
            }
            int v = adj[u][it[u]++];
            if (vis[v]) continue;
            vis[v] = 1;
            ord.push_back(v);
            st.push_back(v);
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m, dir, s;
    cin >> n >> m >> dir >> s;
    Graph g(n, dir);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    g.dfs(s);
    for (int i = 0; i < (int)g.ord.size(); i++) {
        cout << g.ord[i] << (i + 1 == (int)g.ord.size() ? '\n' : ' ');
    }
}

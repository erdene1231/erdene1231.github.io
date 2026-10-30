#include <bits/stdc++.h>
using namespace std;

struct DFS {
    int n, timer;
    vector<vector<int>> adj;
    vector<int> tin, tout, par, pre, post;

    DFS(int _n) {
        n = _n;
        timer = 0;
        adj.resize(n + 1);
        tin.resize(n + 1);
        tout.resize(n + 1);
        par.resize(n + 1);
    }

    void visit(int v) {
        tin[v] = ++timer;
        pre.push_back(v);
        for (int u : adj[v]) {
            if (!tin[u]) {
                par[u] = v;
                visit(u);
            }
        }
        tout[v] = ++timer;
        post.push_back(v);
    }

    int run() {
        int comps = 0;
        for (int v = 1; v <= n; v++) {
            if (!tin[v]) {
                comps++;
                visit(v);
            }
        }
        return comps;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    DFS walk(n);
    while (m--) {
        int a, b;
        cin >> a >> b;
        walk.adj[a].push_back(b);
        walk.adj[b].push_back(a);
    }
    cout << walk.run() << '\n';
    for (int v : walk.pre) cout << v << ' ';
    cout << '\n';
    for (int v : walk.post) cout << v << ' ';
    cout << '\n';
    for (int v = 1; v <= n; v++) {
        cout << walk.par[v] << ' ' << walk.tin[v] << ' ' << walk.tout[v] << '\n';
    }
    return 0;
}

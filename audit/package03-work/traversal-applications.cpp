#include <bits/stdc++.h>
using namespace std;

struct Graph {
    int n, m;
    vector<vector<pair<int, int>>> adj;
    Graph(int _n) {
        n = _n;
        m = 0;
        adj.resize(n + 1);
    }
    void add(int a, int b) {
        adj[a].push_back({b, m});
        adj[b].push_back({a, m});
        m++;
    }
};

vector<int> components(const Graph &g) {
    vector<int> comp(g.n + 1);
    int k = 0;
    for (int s = 1; s <= g.n; s++) {
        if (comp[s]) continue;
        k++;
        vector<int> st = {s};
        comp[s] = k;
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            for (auto [v, id] : g.adj[u]) {
                if (comp[v]) continue;
                comp[v] = k;
                st.push_back(v);
            }
        }
    }
    return comp;
}

bool hasCycle(const Graph &g) {
    vector<int> vis(g.n + 1), pe(g.n + 1, -1);
    for (int s = 1; s <= g.n; s++) {
        if (vis[s]) continue;
        queue<int> q;
        vis[s] = 1;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto [v, id] : g.adj[u]) {
                if (id == pe[u]) continue;
                if (vis[v]) return true;
                vis[v] = 1;
                pe[v] = id;
                q.push(v);
            }
        }
    }
    return false;
}

bool cycleByCount(const Graph &g, const vector<int> &comp) {
    int k = *max_element(comp.begin(), comp.end());
    vector<int> cnt(k + 1), deg(k + 1);
    for (int u = 1; u <= g.n; u++) {
        cnt[comp[u]]++;
        deg[comp[u]] += (int)g.adj[u].size();
    }
    for (int c = 1; c <= k; c++) {
        if (deg[c] / 2 >= cnt[c]) return true;
    }
    return false;
}

vector<int> coloring(const Graph &g) {
    vector<int> col(g.n + 1, -1);
    for (int s = 1; s <= g.n; s++) {
        if (col[s] != -1) continue;
        queue<int> q;
        col[s] = 0;
        q.push(s);
        while (!q.empty()) {
            int u = q.front();
            q.pop();
            for (auto [v, id] : g.adj[u]) {
                if (col[v] == -1) {
                    col[v] = col[u] ^ 1;
                    q.push(v);
                } else if (col[v] == col[u]) return {};
            }
        }
    }
    return col;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    Graph g(n);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        g.add(a, b);
    }
    auto comp = components(g);
    cout << *max_element(comp.begin(), comp.end()) << '\n';
    for (int u = 1; u <= n; u++) cout << comp[u] << (u == n ? '\n' : ' ');
    cout << hasCycle(g) << ' ' << cycleByCount(g, comp) << '\n';
    auto col = coloring(g);
    if (col.empty()) cout << "NOT_BIPARTITE\n";
    else {
        cout << "BIPARTITE\n";
        for (int u = 1; u <= n; u++) cout << col[u] << (u == n ? '\n' : ' ');
    }
}

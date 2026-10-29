#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> topo(const vector<vector<int>> &adj) {
    int n = (int)adj.size() - 1;
    vector<int> state(n + 1), ord;
    for (int s = 1; s <= n; s++) {
        if (state[s]) continue;
        vector<pair<int, int>> st = {{s, 0}};
        state[s] = 1;
        while (!st.empty()) {
            int u = st.back().first;
            int &i = st.back().second;
            if (i == (int)adj[u].size()) {
                state[u] = 2;
                ord.push_back(u);
                st.pop_back();
                continue;
            }
            int v = adj[u][i++];
            if (state[v] == 1) return {};
            if (state[v] == 0) {
                state[v] = 1;
                st.push_back({v, 0});
            }
        }
    }
    reverse(ord.begin(), ord.end());
    return ord;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> adj(n + 1);
    for (int i = 0, a, b; i < m; i++) {
        cin >> a >> b;
        adj[a].push_back(b);
    }
    auto ord = topo(adj);
    if (ord.empty()) cout << "IMPOSSIBLE\n";
    else for (int i = 0; i < n; i++) cout << ord[i] << (i + 1 == n ? '\n' : ' ');
}

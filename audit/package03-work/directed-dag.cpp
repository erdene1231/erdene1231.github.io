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
    int n, m, s, t;
    cin >> n >> m >> s >> t;
    vector<vector<int>> adj(n + 1);
    vector<vector<pair<int, ll>>> edges(n + 1);
    for (int i = 0, a, b; i < m; i++) {
        ll w;
        cin >> a >> b >> w;
        adj[a].push_back(b);
        edges[a].push_back({b, w});
    }
    auto ord = topo(adj);
    if (ord.empty()) {
        cout << "CYCLIC\n";
        return 0;
    }
    const ll INF = 1LL << 62;
    vector<ll> ways(n + 1), back(n + 1);
    vector<ll> low(n + 1, INF), high(n + 1, -INF);
    vector<int> mn(n + 1, n + 1), mx(n + 1, -1);
    ways[s] = 1;
    low[s] = high[s] = mn[s] = mx[s] = 0;
    for (int u : ord) {
        if (ways[u] == 0) continue;
        for (auto [v, w] : edges[u]) {
            ways[v] += ways[u];
            low[v] = min(low[v], low[u] + w);
            high[v] = max(high[v], high[u] + w);
            mn[v] = min(mn[v], mn[u] + 1);
            mx[v] = max(mx[v], mx[u] + 1);
        }
    }
    back[t] = 1;
    for (int i = n - 1; i >= 0; i--) {
        int u = ord[i];
        for (int v : adj[u]) back[u] += back[v];
    }
    cout << ways[t] << '\n';
    if (ways[t] == 0) {
        cout << "UNREACHABLE\nUNREACHABLE\n\n";
        return 0;
    }
    cout << low[t] << ' ' << high[t] << '\n';
    cout << mn[t] << ' ' << mx[t] << '\n';
    for (int u = 1; u <= n; u++) {
        if (ways[u] * back[u] == ways[t]) cout << u << ' ';
    }
    cout << '\n';
}

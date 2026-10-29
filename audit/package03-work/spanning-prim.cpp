#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<pair<int, ll>>> adj(n + 1);
    for (int i = 0; i < m; i++) {
        int a, b;
        ll w;
        cin >> a >> b >> w;
        adj[a].push_back({b, w});
        adj[b].push_back({a, w});
    }
    using State = tuple<ll, int, int>;
    priority_queue<State, vector<State>, greater<State>> q;
    vector<bool> used(n + 1);
    vector<tuple<int, int, ll>> tree;
    q.push({0, 1, 0});
    ll sum = 0;
    int cnt = 0;
    while (!q.empty()) {
        auto [w, u, p] = q.top();
        q.pop();
        if (used[u]) continue;
        used[u] = true;
        cnt++;
        sum += w;
        if (p != 0) tree.push_back({p, u, w});
        for (auto [v, cost] : adj[u]) {
            if (!used[v]) q.push({cost, v, u});
        }
    }
    if (cnt != n) {
        cout << "IMPOSSIBLE\n";
        return 0;
    }
    cout << sum << '\n';
    for (auto [a, b, w] : tree) cout << a << ' ' << b << ' ' << w << '\n';
}

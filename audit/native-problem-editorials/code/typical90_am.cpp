#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<int>> g(n);
    for (int i = 0; i < n - 1; ++i) {
        int a, b;
        cin >> a >> b;
        --a;
        --b;
        g[a].push_back(b);
        g[b].push_back(a);
    }
    vector<int> parent(n, -1), order{0};
    for (int i = 0; i < n; ++i) {
        int u = order[i];
        for (int v : g[u]) {
            if (v == parent[u]) continue;
            parent[v] = u;
            order.push_back(v);
        }
    }
    vector<ll> sub(n, 1);
    ll ans = 0;
    for (int i = n - 1; i > 0; --i) {
        int u = order[i];
        ans += sub[u] * (n - sub[u]);
        sub[parent[u]] += sub[u];
    }
    cout << ans << '\n';
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<vector<int>> g(n), rev(n);
    for (int i = 0; i < m; ++i) {
        int a, b;
        cin >> a >> b;
        --a;
        --b;
        g[a].push_back(b);
        rev[b].push_back(a);
    }
    vector<char> seen(n);
    vector<int> order;
    for (int start = 0; start < n; ++start) {
        if (seen[start]) continue;
        vector<pair<int, int>> st{{start, 0}};
        seen[start] = true;
        while (!st.empty()) {
            int u = st.back().first;
            int edge = st.back().second;
            if (edge == int(g[u].size())) {
                order.push_back(u);
                st.pop_back();
                continue;
            }
            ++st.back().second;
            int v = g[u][edge];
            if (!seen[v]) {
                seen[v] = true;
                st.push_back({v, 0});
            }
        }
    }
    fill(seen.begin(), seen.end(), false);
    ll ans = 0;
    for (auto it = order.rbegin(); it != order.rend(); ++it) {
        int start = *it;
        if (seen[start]) continue;
        vector<int> st{start};
        seen[start] = true;
        ll size = 0;
        while (!st.empty()) {
            int u = st.back();
            st.pop_back();
            ++size;
            for (int v : rev[u]) {
                if (seen[v]) continue;
                seen[v] = true;
                st.push_back(v);
            }
        }
        ans += size * (size - 1) / 2;
    }
    cout << ans << '\n';
}

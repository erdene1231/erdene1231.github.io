#include <bits/stdc++.h>
using namespace std;

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
    vector<int> color(n, -1);
    array<vector<int>, 2> group;
    queue<int> q;
    q.push(0);
    color[0] = 0;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        group[color[u]].push_back(u);
        for (int v : g[u]) {
            if (color[v] != -1) continue;
            color[v] = color[u] ^ 1;
            q.push(v);
        }
    }
    int side = group[0].size() >= size_t(n / 2) ? 0 : 1;
    for (int i = 0; i < n / 2; ++i) {
        cout << group[side][i] + 1 << (i + 1 == n / 2 ? '\n' : ' ');
    }
}

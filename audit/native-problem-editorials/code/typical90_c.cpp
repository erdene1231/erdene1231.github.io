#include <bits/stdc++.h>
using namespace std;

pair<int, int> farthest(const vector<vector<int>> &g, int start) {
    vector<int> dist(g.size(), -1);
    queue<int> q;
    q.push(start);
    dist[start] = 0;
    int best = start;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        if (dist[u] > dist[best]) best = u;
        for (int v : g[u]) {
            if (dist[v] != -1) continue;
            dist[v] = dist[u] + 1;
            q.push(v);
        }
    }
    return {best, dist[best]};
}

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
    int u = farthest(g, 0).first;
    int diameter = farthest(g, u).second;
    cout << diameter + 1 << '\n';
}

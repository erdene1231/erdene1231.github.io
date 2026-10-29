#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h, w;
    cin >> h >> w;
    int n = h * w, b = max(1, (int) sqrt(n)), ans = n + 1;
    map<string, vector<int>> groups;
    for (int v = 0; v < n; v++) {
        string c;
        cin >> c;
        groups[c].push_back(v);
    }
    auto distance = [&](int u, int v) {
        return abs(u / w - v / w) + abs(u % w - v % w);
    };
    for (auto &[c, pos] : groups) {
        int k = (int) pos.size();
        if (k < 2) continue;
        if (k <= b) {
            for (int i = 0; i < k; i++) {
                for (int j = i + 1; j < k; j++) {
                    ans = min(ans, distance(pos[i], pos[j]));
                }
            }
            continue;
        }
        vector<int> dist(n, -1), owner(n, -1);
        queue<int> q;
        for (int v : pos) {
            dist[v] = 0;
            owner[v] = v;
            q.push(v);
        }
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            int r = v / w, s = v % w;
            for (auto [dr, dc] : vector<pair<int, int>>{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}) {
                int nr = r + dr, nc = s + dc;
                if (nr < 0 || nr >= h || nc < 0 || nc >= w) continue;
                int u = nr * w + nc;
                if (dist[u] == -1) {
                    dist[u] = dist[v] + 1;
                    owner[u] = owner[v];
                    q.push(u);
                } else if (owner[u] != owner[v]) {
                    ans = min(ans, dist[u] + dist[v] + 1);
                }
            }
        }
    }
    cout << (ans == n + 1 ? -1 : ans) << '\n';
}

#include <bits/stdc++.h>
using namespace std;

struct Paint {
    int h, w, n, b;
    vector<int> black, dist, pending;

    Paint(int _h, int _w, int start) {
        h = _h;
        w = _w;
        n = h * w;
        b = max(1, (int) sqrt(n));
        black.assign(n, 0);
        black[start] = 1;
        rebuild();
    }
    void rebuild() {
        dist.assign(n, -1);
        queue<int> q;
        for (int v = 0; v < n; v++) {
            if (black[v]) {
                dist[v] = 0;
                q.push(v);
            }
        }
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (auto [dr, dc] : vector<pair<int, int>>{{-1, 0}, {1, 0}, {0, -1}, {0, 1}}) {
                int r = v / w + dr, c = v % w + dc;
                if (r < 0 || r >= h || c < 0 || c >= w) continue;
                int u = r * w + c;
                if (dist[u] != -1) continue;
                dist[u] = dist[v] + 1;
                q.push(u);
            }
        }
        pending.clear();
    }
    int add(int v) {
        int ans = dist[v];
        for (int u : pending) {
            ans = min(ans, abs(v / w - u / w) + abs(v % w - u % w));
        }
        black[v] = 1;
        pending.push_back(v);
        if ((int) pending.size() == b) rebuild();
        return ans;
    }
};
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h, w, q, r, c;
    cin >> h >> w >> q >> r >> c;
    Paint st(h, w, r * w + c);
    while (q--) {
        cin >> r >> c;
        cout << st.add(r * w + c) << '\n';
    }
}

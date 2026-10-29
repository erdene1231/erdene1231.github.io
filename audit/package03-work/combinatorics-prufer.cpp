#include <bits/stdc++.h>
using namespace std;
using ll = long long;

const int MOD = 1000000007;

ll modpow(ll a, int n) {
    ll res = 1;
    while (n) {
        if (n & 1) res = res * a % MOD;
        a = a * a % MOD;
        n >>= 1;
    }
    return res;
}

struct Prufer {
    int n;
    vector<vector<int>> adj;

    Prufer(int _n) {
        n = _n;
        adj.resize(n + 1);
    }

    void add(int a, int b) {
        adj[a].push_back(b);
        adj[b].push_back(a);
    }

    vector<int> encode() {
        vector<int> deg(n + 1), code;
        priority_queue<int, vector<int>, greater<int>> q;
        for (int u = 1; u <= n; u++) {
            deg[u] = adj[u].size();
            if (deg[u] == 1) q.push(u);
        }
        for (int i = 0; i < n - 2; i++) {
            int u = q.top();
            q.pop();
            for (int v : adj[u]) {
                if (deg[v] == 0) continue;
                code.push_back(v);
                deg[u] = 0;
                if (--deg[v] == 1) q.push(v);
                break;
            }
        }
        return code;
    }

    vector<pair<int, int>> decode(const vector<int> &code) {
        vector<int> deg(n + 1, 1);
        vector<pair<int, int>> edges;
        if (n == 1) return edges;
        for (int v : code) deg[v]++;
        priority_queue<int, vector<int>, greater<int>> q;
        for (int u = 1; u <= n; u++) if (deg[u] == 1) q.push(u);
        for (int v : code) {
            int u = q.top();
            q.pop();
            edges.push_back({u, v});
            deg[u]--;
            if (--deg[v] == 1) q.push(v);
        }
        int a = q.top();
        q.pop();
        edges.push_back({a, q.top()});
        return edges;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    char mode;
    int n;
    cin >> mode >> n; // 1 <= n <= 200000
    Prufer t(n);
    vector<int> code;
    if (mode == 'E') { // input is a valid labeled tree
        for (int i = 1; i < n; i++) {
            int a, b;
            cin >> a >> b;
            t.add(a, b);
        }
        code = t.encode();
    } else { // D: n-2 labels in 1..n; empty for n=1,2
        code.resize(max(0, n - 2));
        for (int &v : code) cin >> v;
    }
    auto edges = t.decode(code);
    cout << (n == 1 ? 1 : modpow(n, n - 2)) << "\n";
    cout << code.size();
    for (int v : code) cout << ' ' << v;
    cout << "\n" << edges.size() << "\n";
    for (auto [a, b] : edges) cout << a << ' ' << b << "\n";
}

#include <bits/stdc++.h>
using namespace std;

struct Components {
    int n;
    vector<vector<int>> adj;
    vector<int> id, sz, rep;

    Components(int _n) {
        n = _n;
        adj.resize(n + 1);
        id.assign(n + 1, -1);
    }

    void fill(int s) {
        int c = rep.size();
        rep.push_back(s);
        sz.push_back(0);
        vector<int> st = {s};
        id[s] = c;
        while (!st.empty()) {
            int v = st.back();
            st.pop_back();
            sz[c]++;
            for (int u : adj[v]) {
                if (id[u] == -1) {
                    id[u] = c;
                    st.push_back(u);
                }
            }
        }
    }

    void run() {
        for (int v = 1; v <= n; v++) {
            if (id[v] == -1) fill(v);
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    Components cc(n);
    while (m--) {
        int a, b;
        cin >> a >> b;
        cc.adj[a].push_back(b);
        cc.adj[b].push_back(a);
    }
    cc.run();
    int k = cc.rep.size();
    cout << (k == 0 ? 0 : k - 1) << '\n';
    for (int i = 1; i < k; i++) {
        cout << cc.rep[0] << ' ' << cc.rep[i] << '\n';
    }
    return 0;
}

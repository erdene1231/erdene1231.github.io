#include <bits/stdc++.h>
using namespace std;

struct BinaryTree {
    int n;
    vector<int> lc, rc;
    BinaryTree(int _n) {
        n = _n;
        lc.resize(n + 1);
        rc.resize(n + 1);
    }
    vector<vector<int>> orders(int root) {
        vector<vector<int>> res(3);
        vector<pair<int, int>> st = {{root, 0}};
        while (!st.empty()) {
            auto [u, phase] = st.back();
            st.pop_back();
            if (u == 0) continue;
            if (phase == 0) {
                res[0].push_back(u);
                st.push_back({u, 1});
                st.push_back({lc[u], 0});
            } else if (phase == 1) {
                res[1].push_back(u);
                st.push_back({u, 2});
                st.push_back({rc[u], 0});
            } else res[2].push_back(u);
        }
        return res;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, root;
    cin >> n >> root;
    BinaryTree g(n);
    for (int u = 1; u <= n; u++) cin >> g.lc[u] >> g.rc[u];
    auto orders = g.orders(root);
    for (const auto &a : orders) {
        for (int u : a) cout << u << ' ';
        cout << '\n';
    }
}

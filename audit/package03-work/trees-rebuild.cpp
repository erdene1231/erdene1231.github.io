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
    int fromPre(const vector<int> &pre, const vector<int> &in) {
        fill(lc.begin(), lc.end(), 0);
        fill(rc.begin(), rc.end(), 0);
        if (n == 0) return 0;
        vector<int> st = {pre[0]};
        int k = 0;
        for (int i = 1; i < n; i++) {
            int u = pre[i], p = st.back();
            if (p != in[k]) lc[p] = u;
            else {
                while (!st.empty() && k < n && st.back() == in[k]) {
                    p = st.back();
                    st.pop_back();
                    k++;
                }
                rc[p] = u;
            }
            st.push_back(u);
        }
        return pre[0];
    }
    int fromPost(vector<int> post, vector<int> in) {
        reverse(post.begin(), post.end());
        reverse(in.begin(), in.end());
        int root = fromPre(post, in);
        for (int u = 1; u <= n; u++) swap(lc[u], rc[u]);
        return root;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    string mode;
    cin >> n >> mode;
    vector<int> seq(n), in(n);
    for (int &u : seq) cin >> u;
    for (int &u : in) cin >> u;
    BinaryTree g(n);
    int root = mode == "PRE" ? g.fromPre(seq, in) : g.fromPost(seq, in);
    cout << root << '\n';
    for (int u = 1; u <= n; u++) cout << g.lc[u] << ' ' << g.rc[u] << '\n';
}

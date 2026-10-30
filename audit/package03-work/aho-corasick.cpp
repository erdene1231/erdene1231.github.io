#include <bits/stdc++.h>
using namespace std;

struct Aho {
    struct Node {
        array<int, 26> go;
        int link = 0, out = 0;
        vector<int> ids;
        Node() {
            go.fill(-1);
        }
    };
    vector<Node> t;
    vector<int> tail, order;
    Aho(int n) {
        t.reserve(n + 1);
        t.emplace_back();
    }
    void add(const string& s) {
        int v = 0;
        for (char ch : s) {
            int c = ch - 'a';
            if (t[v].go[c] == -1) {
                int u = (int)t.size();
                t.emplace_back();
                t[v].go[c] = u;
            }
            v = t[v].go[c];
        }
        t[v].ids.push_back((int)tail.size());
        tail.push_back(v);
    }
    void build() {
        queue<int> q;
        for (int c = 0; c < 26; c++) {
            int u = t[0].go[c];
            if (u == -1) t[0].go[c] = 0;
            else q.push(u);
        }
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            order.push_back(v);
            int f = t[v].link;
            t[v].out = t[f].ids.empty() ? t[f].out : f;
            for (int c = 0; c < 26; c++) {
                int u = t[v].go[c];
                if (u == -1) t[v].go[c] = t[f].go[c];
                else {
                    t[u].link = t[f].go[c];
                    q.push(u);
                }
            }
        }
    }
    vector<int> count(const string& s) const {
        vector<int> cnt(t.size());
        int v = 0;
        for (char ch : s) {
            v = t[v].go[ch - 'a'];
            cnt[v]++;
        }
        for (int i = (int)order.size() - 1; i >= 0; i--) {
            int u = order[i];
            cnt[t[u].link] += cnt[u];
        }
        vector<int> ans;
        for (int u : tail) ans.push_back(cnt[u]);
        return ans;
    }
    void report(const string& s) const {
        int v = 0;
        for (int i = 0; i < (int)s.size(); i++) {
            v = t[v].go[s[i] - 'a'];
            int u = t[v].ids.empty() ? t[v].out : v;
            while (u != 0) {
                for (int id : t[u].ids) {
                    cout << i + 1 << ' ' << id + 1 << '\n';
                }
                u = t[u].out;
            }
        }
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    int k;
    cin >> s >> k;
    vector<string> p(k);
    int m = 0;
    for (string& x : p) {
        cin >> x;
        m += (int)x.size();
    }
    Aho ac(m);
    for (const string& x : p) ac.add(x);
    ac.build();
    for (int x : ac.count(s)) cout << x << '\n';
}

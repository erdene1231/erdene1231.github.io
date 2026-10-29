#include <bits/stdc++.h>
using namespace std;

struct Huffman {
    int n, root;
    vector<int> w;
    vector<int> l, r;
    vector<string> code;

    Huffman(int _n) {
        n = _n;
        root = -1;
        w.resize(2 * n);
        l.assign(2 * n, -1);
        r.assign(2 * n, -1);
        code.resize(n);
    }

    void dfs(int v, string s) {
        if (v < n) {
            code[v] = s.empty() ? "0" : s;
            return;
        }
        dfs(l[v], s + '0');
        dfs(r[v], s + '1');
    }

    void build(const vector<int>& freq) {
        priority_queue<pair<int, int>, vector<pair<int, int>>,
                       greater<pair<int, int>>> q;
        int cnt = n;
        for (int i = 0; i < n; i++) {
            w[i] = freq[i];
            if (w[i] > 0) q.push({w[i], i});
        }
        while (q.size() > 1) {
            auto [a, u] = q.top(); q.pop();
            auto [b, v] = q.top(); q.pop();
            if (u > v) swap(u, v);
            w[cnt] = a + b;
            l[cnt] = u;
            r[cnt] = v;
            q.push({w[cnt], cnt});
            cnt++;
        }
        root = q.empty() ? -1 : q.top().second;
        if (root != -1) dfs(root, "");
    }

    string encode(const string& s) const {
        string bits;
        for (char c : s) bits += code[c - 'A'];
        return bits;
    }

    string decode(const string& bits) const {
        string s;
        if (root == -1) return s;
        if (root < n) return string(bits.size(), char('A' + root));
        int v = root;
        for (char b : bits) {
            v = (b == '0' ? l[v] : r[v]);
            if (v < n) {
                s += char('A' + v);
                v = root;
            }
        }
        return s;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    if (!(cin >> s)) return 0;
    vector<int> freq(26);
    for (char c : s) freq[c - 'A']++;
    Huffman h(26);
    h.build(freq);
    for (int i = 0; i < 26; i++) {
        if (freq[i]) cout << char('A' + i) << ' ' << h.code[i] << '\n';
    }
    string bits = h.encode(s);
    cout << bits << '\n' << bits.size() << '\n' << h.decode(bits) << '\n';
}

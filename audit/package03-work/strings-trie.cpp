#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Trie {
    vector<array<int, 26>> nxt;
    vector<int> term, cnt;
    Trie(int cap) {
        nxt.reserve(cap);
        term.reserve(cap);
        cnt.reserve(cap);
        node();
    }
    int node() {
        int u = (int)nxt.size();
        nxt.emplace_back();
        nxt.back().fill(-1);
        term.push_back(0);
        cnt.push_back(0);
        return u;
    }
    int find(const string &s) const {
        int u = 0;
        for (char c : s) {
            u = nxt[u][c - 'A'];
            if (u == -1) return -1;
        }
        return u;
    }
    bool contains(const string &s) const {
        int u = find(s);
        return u != -1 && term[u];
    }
    void add(const string &s) {
        if (contains(s)) return;
        int u = 0;
        cnt[u]++;
        for (char c : s) {
            int x = c - 'A';
            if (nxt[u][x] == -1) {
                int v = node();
                nxt[u][x] = v;
            }
            u = nxt[u][x];
            cnt[u]++;
        }
        term[u] = 1;
    }
    int prefix_count(const string &s) const {
        int u = find(s);
        return u == -1 ? 0 : cnt[u];
    }
    int longest(const string &s) const {
        int u = 0, best = term[0] ? 0 : -1;
        for (int i = 0; i < (int)s.size(); i++) {
            u = nxt[u][s[i] - 'A'];
            if (u == -1) break;
            if (term[u]) best = i + 1;
        }
        return best;
    }
};

int main() {
    int n, cap = 1;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    vector<string> words(n);
    for (auto &s : words) {
        getline(cin, s);
        cap += (int)s.size();
    }
    Trie t(cap);
    for (const auto &s : words) t.add(s);
    int q;
    cin >> q;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    while (q--) {
        string line;
        getline(cin, line);
        char op = line[0];
        string s = line.size() > 1 ? line.substr(2) : "";
        if (op == 'C') cout << t.contains(s) << '\n';
        else if (op == 'P') cout << t.prefix_count(s) << '\n';
        else cout << t.longest(s) << '\n';
    }
}

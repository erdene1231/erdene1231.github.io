#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Hash {
    int base, mod;
    vector<int> h, p;
    Hash(const string &s, int _base, int _mod) : base(_base), mod(_mod), h(s.size() + 1), p(s.size() + 1, 1) {
        for (int i = 0; i < (int)s.size(); i++) {
            h[i + 1] = (1LL * h[i] * base + (unsigned char)s[i]) % mod;
            p[i + 1] = 1LL * p[i] * base % mod;
        }
    }
    int get(int l, int r) const {
        return (h[r] - 1LL * h[l] * p[r - l] % mod + mod) % mod;
    }
};

struct DHash {
    Hash a, b;
    DHash(const string &s) : a(s, 911382323, 1000000007), b(s, 97266353, 1000000009) {}
    pair<int, int> get(int l, int r) const {
        return {a.get(l, r), b.get(l, r)};
    }
};

vector<int> matches(const string &s, const string &p, bool verify) {
    int n = (int)s.size(), m = (int)p.size();
    DHash hs(s), hp(p);
    auto target = hp.get(0, m);
    vector<int> ans;
    for (int i = 0; i + m <= n; i++) {
        if (hs.get(i, i + m) == target && (!verify || s.compare(i, m, p) == 0)) ans.push_back(i);
    }
    return ans;
}

int main() {
    char mode;
    cin >> mode;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    string s, p;
    getline(cin, s);
    getline(cin, p);
    auto ans = matches(s, p, mode == 'V');
    cout << (mode == 'V' ? "EXACT" : "CANDIDATES") << ' ' << ans.size();
    for (int x : ans) cout << ' ' << x;
    cout << '\n';
}

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

int main() {
    char mode;
    cin >> mode;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    string s;
    getline(cin, s);
    string rev = s;
    reverse(rev.begin(), rev.end());
    DHash a(s), b(rev);
    int n = (int)s.size(), q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        bool same = a.get(l, r) == b.get(n - r, n - l);
        if (same && mode == 'V') {
            for (int i = l, j = r - 1; i < j; i++, j--) {
                if (s[i] != s[j]) {
                    same = false;
                    break;
                }
            }
        }
        cout << (same ? mode == 'V' ? "YES" : "POSSIBLE" : "NO") << '\n';
    }
}

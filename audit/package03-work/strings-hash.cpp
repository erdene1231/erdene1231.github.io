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

int main() {
    string s;
    getline(cin, s);
    int base, mod, q;
    cin >> base >> mod >> q;
    Hash h(s, base, mod);
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << h.get(l, r) << '\n';
    }
}

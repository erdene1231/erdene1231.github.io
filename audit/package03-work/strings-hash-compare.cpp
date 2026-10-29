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

int lcp(const DHash &h, int l, int r, int a, int b) {
    int lo = 0, hi = min(r - l, b - a);
    while (lo < hi) {
        int mid = lo + (hi - lo + 1) / 2;
        if (h.get(l, l + mid) == h.get(a, a + mid)) lo = mid;
        else hi = mid - 1;
    }
    return lo;
}

int main() {
    char mode;
    cin >> mode;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    string s;
    getline(cin, s);
    DHash h(s);
    int q;
    cin >> q;
    while (q--) {
        int l, r, a, b;
        cin >> l >> r >> a >> b;
        int k = lcp(h, l, r, a, b);
        if (mode == 'V') {
            k = 0;
            while (l + k < r && a + k < b && s[l + k] == s[a + k]) k++;
        }
        int cmp;
        if (l + k == r || a + k == b) cmp = ((r - l) > (b - a)) - ((r - l) < (b - a));
        else cmp = ((unsigned char)s[l + k] > (unsigned char)s[a + k]) ? 1 : -1;
        cout << (mode == 'V' ? "EXACT" : "ESTIMATE") << ' ' << k << ' ' << cmp << '\n';
    }
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Window {
    static constexpr array<ll, 2> mod = {1000000007, 1000000009};
    static constexpr array<ll, 2> base = {911382323, 97266353};
    array<ll, 2> h = {}, p = {1, 1};
    Window(const string &s, int m) {
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < 2; j++) {
                h[j] = (h[j] * base[j] + (unsigned char)s[i]) % mod[j];
                if (i + 1 < m) p[j] = p[j] * base[j] % mod[j];
            }
        }
    }
    void shift(unsigned char out, unsigned char in) {
        for (int j = 0; j < 2; j++) {
            h[j] = (h[j] - out * p[j] % mod[j] + mod[j]) % mod[j];
            h[j] = (h[j] * base[j] + in) % mod[j];
        }
    }
};

vector<int> matches(const string &s, const string &p, bool verify) {
    int n = (int)s.size(), m = (int)p.size();
    vector<int> ans;
    if (m == 0) {
        for (int i = 0; i <= n; i++) ans.push_back(i);
        return ans;
    }
    if (m > n) return ans;
    Window window(s, m), target(p, m);
    for (int i = 0; i + m <= n; i++) {
        if (i) window.shift(s[i - 1], s[i + m - 1]);
        if (window.h == target.h && (!verify || s.compare(i, m, p) == 0)) ans.push_back(i);
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

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct SuffixArray {
    int n;
    vector<int> sa, rank, lcp;
    SuffixArray(const string& s) {
        n = (int)s.size();
        sa.resize(n);
        rank.resize(n);
        for (int i = 0; i < n; i++) {
            sa[i] = i;
            rank[i] = (unsigned char)s[i];
        }
        vector<int> nr(n);
        for (int len = 1; len < n; ) {
            auto key = [&](int i) {
                return pair<int, int>{rank[i], i < n - len ? rank[i + len] : -1};
            };
            sort(sa.begin(), sa.end(), [&](int a, int b) {
                return key(a) < key(b);
            });
            nr[sa[0]] = 0;
            for (int i = 1; i < n; i++) {
                nr[sa[i]] = nr[sa[i - 1]] + (key(sa[i - 1]) != key(sa[i]));
            }
            rank.swap(nr);
            if (rank[sa[n - 1]] == n - 1 || len >= n - len) break;
            len *= 2;
        }
        for (int i = 0; i < n; i++) rank[sa[i]] = i;
        lcp.assign(n, 0);
        int h = 0;
        for (int i = 0; i < n; i++) {
            int r = rank[i];
            if (r == 0) {
                h = 0;
                continue;
            }
            int j = sa[r - 1];
            while (i + h < n && j + h < n && s[i + h] == s[j + h]) h++;
            lcp[r] = h;
            if (h > 0) h--;
        }
    }
    ll distinct() const {
        ll ans = 1LL * n * (n + 1) / 2;
        for (int x : lcp) ans -= x;
        return ans;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    getline(cin, s);
    SuffixArray a(s);
    for (int i = 0; i < a.n; i++) {
        cout << a.sa[i] << ' ' << a.lcp[i] << '\n';
    }
    cout << a.distinct() << '\n';
}

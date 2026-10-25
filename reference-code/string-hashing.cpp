#include <bits/stdc++.h>
using namespace std;

const long long MOD1 = 1000000007;
const long long MOD2 = 1000000009;
const long long BASE = 911382323;

long long get_hash(const vector<long long>& h,
                   const vector<long long>& power,
                   int l, int r, long long mod) {
    return (h[r] - h[l] * power[r - l] % mod + mod) % mod;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    string s;
    int q;
    cin >> s >> q;
    int n = s.size();
    vector<long long> h1(n + 1), h2(n + 1);
    vector<long long> p1(n + 1, 1), p2(n + 1, 1);
    for (int i = 0; i < n; i++) {
        int value = s[i] - 'a' + 1;
        h1[i + 1] = (h1[i] * BASE + value) % MOD1;
        h2[i + 1] = (h2[i] * BASE + value) % MOD2;
        p1[i + 1] = p1[i] * BASE % MOD1;
        p2[i + 1] = p2[i] * BASE % MOD2;
    }

    while (q--) {
        int l1, r1, l2, r2;
        cin >> l1 >> r1 >> l2 >> r2;
        l1--;
        l2--;
        bool equal = r1 - l1 == r2 - l2;
        equal = equal && get_hash(h1, p1, l1, r1, MOD1) == get_hash(h1, p1, l2, r2, MOD1);
        equal = equal && get_hash(h2, p2, l1, r1, MOD2) == get_hash(h2, p2, l2, r2, MOD2);
        cout << (equal ? "YES" : "NO") << '\n';
    }

    return 0;
}

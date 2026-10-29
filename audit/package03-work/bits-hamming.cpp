#include <bits/stdc++.h>
using namespace std;

using ull = unsigned long long;

int direct(const string& a, const string& b) {
    int d = 0;
    for (int i = 0; i < (int)a.size(); i++) d += a[i] != b[i];
    return d;
}
ull pack(const string& s) {
    ull x = 0;
    for (char c : s) x = (x << 1) | (c - '0');
    return x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<string> s(n);
    vector<ull> a(n);
    for (int i = 0; i < n; i++) {
        cin >> s[i];
        a[i] = pack(s[i]);
    }
    int slow = k + 1, fast = k + 1;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j < n; j++) {
            slow = min(slow, direct(s[i], s[j]));
            fast = min(fast, __builtin_popcountll(a[i] ^ a[j]));
        }
    }
    cout << slow << ' ' << fast << '\n';
}

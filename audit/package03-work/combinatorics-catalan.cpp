#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll catalan(int n) {
    vector<ll> c(n + 1);
    c[0] = 1;
    for (int s = 1; s <= n; s++) {
        for (int i = 0; i < s; i++) c[s] += c[i] * c[s - i - 1];
    }
    return c[n];
}

ll closed(int n) {
    vector<ll> c(2 * n + 2);
    c[0] = 1;
    for (int i = 1; i <= 2 * n; i++) {
        for (int j = i; j >= 1; j--) c[j] += c[j - 1];
    }
    return c[n] - c[n + 1];
}

void generate(int n, int l, int r, string &s) {
    if (l == n && r == n) {
        cout << s << "\n";
        return;
    }
    if (l < n) {
        s += '(';
        generate(n, l + 1, r, s);
        s.pop_back();
    }
    if (r < l) {
        s += ')';
        generate(n, l, r + 1, s);
        s.pop_back();
    }
}

int main() {
    int n;
    cin >> n; // 0 <= n <= 30
    cout << catalan(n) << ' ' << closed(n) << "\n";
    if (n <= 8) {
        string s;
        generate(n, 0, 0, s);
    }
}

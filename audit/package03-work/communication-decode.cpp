#include <bits/stdc++.h>
using namespace std;

optional<int> decode(const string& s) {
    if (s.size() != 13) return nullopt;
    int x = 0, parity = 0;
    for (int i = 0; i < 13; i++) {
        if (s[i] != '0' && s[i] != '1') return nullopt;
        int b = s[i] - '0';
        parity ^= b;
        if (i < 12) x |= b << i;
    }
    if (parity != 0) return nullopt;
    return x;
}

int main() {
    string s;
    if (!(cin >> s)) {
        cout << "INVALID\n";
        return 0;
    }
    auto x = decode(s);
    if (!x) cout << "INVALID\n";
    else cout << *x << '\n';
}

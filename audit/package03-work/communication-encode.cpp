#include <bits/stdc++.h>
using namespace std;

string encode(int x) {
    string s;
    int parity = 0;
    for (int i = 0; i < 12; i++) {
        int b = (x >> i) & 1;
        s += char('0' + b);
        parity ^= b;
    }
    s += char('0' + parity);
    return s;
}

int main() {
    int x;
    if (!(cin >> x) || x < 0 || x >= 4096) {
        cout << "INVALID\n";
        return 0;
    }
    cout << encode(x) << '\n';
}

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    if (n % 2) return 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        int bal = 0;
        bool ok = true;
        string s;
        for (int i = n - 1; i >= 0; --i) {
            bool close = (mask >> i) & 1;
            s += close ? ')' : '(';
            bal += close ? -1 : 1;
            if (bal < 0) {
                ok = false;
                break;
            }
        }
        if (ok && bal == 0) cout << s << '\n';
    }
}

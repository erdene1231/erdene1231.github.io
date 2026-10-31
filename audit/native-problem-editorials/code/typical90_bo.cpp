#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    int k;
    cin >> s >> k;
    while (k--) {
        ll value = 0;
        for (char c : s) value = value * 8 + (c - '0');
        string next;
        do {
            int digit = int(value % 9);
            if (digit == 8) digit = 5;
            next.push_back(char('0' + digit));
            value /= 9;
        } while (value > 0);
        reverse(next.begin(), next.end());
        s = next;
    }
    cout << s << '\n';
}

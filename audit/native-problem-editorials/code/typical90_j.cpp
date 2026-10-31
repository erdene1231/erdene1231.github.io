#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<array<int, 2>> pref(n + 1);
    for (int i = 1; i <= n; ++i) {
        int c, p;
        cin >> c >> p;
        pref[i] = pref[i - 1];
        pref[i][c - 1] += p;
    }
    int q;
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << pref[r][0] - pref[l - 1][0] << ' '
             << pref[r][1] - pref[l - 1][1] << '\n';
    }
}

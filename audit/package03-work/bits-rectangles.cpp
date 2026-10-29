#include <bits/stdc++.h>
using namespace std;

using ll = long long;

ll direct(const vector<string>& a) {
    int n = a.size();
    ll ans = 0;
    for (int r = 0; r < n; r++) {
        for (int s = r + 1; s < n; s++) {
            int c = 0;
            for (int j = 0; j < n; j++) c += a[r][j] == '1' && a[s][j] == '1';
            ans += 1LL * c * (c - 1) / 2;
        }
    }
    return ans;
}

ll packed(const vector<string>& a) {
    int n = a.size(), blocks = (n + 63) / 64;
    vector<vector<unsigned long long>> bits(n, vector<unsigned long long>(blocks));
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            if (a[i][j] == '1') bits[i][j / 64] |= 1ULL << (j % 64);
        }
    }
    ll ans = 0;
    for (int r = 0; r < n; r++) {
        for (int s = r + 1; s < n; s++) {
            int c = 0;
            for (int j = 0; j < blocks; j++) c += __builtin_popcountll(bits[r][j] & bits[s][j]);
            ans += 1LL * c * (c - 1) / 2;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, mode;
    cin >> n >> mode;
    vector<string> a(n);
    for (string& row : a) cin >> row;
    if (mode == 1) cout << direct(a) << '\n';
    else cout << packed(a) << '\n';
}

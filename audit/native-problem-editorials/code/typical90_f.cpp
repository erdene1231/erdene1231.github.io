#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    string s;
    cin >> n >> k >> s;
    vector<array<int, 26>> nxt(n + 1);
    nxt[n].fill(n);
    for (int i = n - 1; i >= 0; --i) {
        nxt[i] = nxt[i + 1];
        nxt[i][s[i] - 'a'] = i;
    }
    string ans;
    int pos = 0;
    for (int used = 0; used < k; ++used) {
        int need = k - used - 1;
        for (int c = 0; c < 26; ++c) {
            int at = nxt[pos][c];
            if (at < n && n - at - 1 >= need) {
                ans += char('a' + c);
                pos = at + 1;
                break;
            }
        }
    }
    cout << ans << '\n';
}

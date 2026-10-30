#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DigitDP {
    string s;
    ll dp[20][11][2];
    ll dfs(int pos, int prev, bool tight, bool started) {
        if (pos == (int)s.size()) return 1;
        if (!tight && dp[pos][prev][started] != -1) {
            return dp[pos][prev][started];
        }
        int limit = tight ? s[pos] - '0' : 9;
        ll ans = 0;
        for (int d = 0; d <= limit; d++) {
            if (started && d == prev) continue;
            bool nt = tight && d == s[pos] - '0';
            bool ns = started || d != 0;
            int np = ns ? d : 10;
            ans += dfs(pos + 1, np, nt, ns);
        }
        if (!tight) dp[pos][prev][started] = ans;
        return ans;
    }
    ll count(ll x) {
        if (x < 0) return 0;
        s = to_string(x);
        for (auto& row : dp) {
            for (auto& cell : row) cell[0] = cell[1] = -1;
        }
        return dfs(0, 10, true, false);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll a, b;
    cin >> a >> b;
    DigitDP digit;
    ll hi = digit.count(b);
    ll lo = digit.count(a - 1);
    cout << hi - lo << '\n';
}

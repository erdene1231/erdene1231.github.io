#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<long double> binomial(int n, long double p) {
    vector<long double> dp(n + 1);
    dp[0] = 1;
    for (int i = 0; i < n; i++) {
        for (int j = i + 1; j >= 0; j--) {
            dp[j] = dp[j] * (1 - p) + (j ? dp[j - 1] * p : 0);
        }
    }
    return dp;
}

int main() {
    char mode;
    cin >> mode;
    cout << fixed << setprecision(18);
    if (mode == 'B') {
        int n;
        long double p;
        cin >> n >> p;
        for (auto x : binomial(n, p)) cout << x << ' ';
        cout << '\n' << n * p << '\n';
    } else if (mode == 'G') {
        long double p;
        ll k;
        cin >> p >> k;
        if (p == 0) cout << "0 INF\n";
        else {
            long double mass = k == 1 ? p : powl(1 - p, k - 1) * p;
            cout << mass << ' ' << 1 / p << '\n';
        }
    } else if (mode == 'C') {
        ll n;
        long double p;
        cin >> n >> p;
        long double ans = n == 0 ? 0 : p == 1 ? 1 : -expm1l(n * log1pl(-p));
        cout << ans << '\n';
    } else if (mode == 'E') {
        ll n;
        cin >> n;
        long double ans = n == 1 ? 0 : n * expl(n * log1pl(-1.L / n));
        cout << ans << '\n';
    } else if (mode == 'U') {
        ll a, b;
        cin >> a >> b;
        cout << ((long double)a + b) / 2 << '\n';
    }
}

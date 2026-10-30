#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int minRides(const vector<ll> &w, ll x) {
    int n = w.size();
    int m = 1 << n;
    vector<pair<int, ll>> best(m, {n + 1, 0});
    best[0] = {1, 0};
    for (int s = 1; s < m; s++) {
        for (int i = 0; i < n; i++) {
            if (s & (1 << i)) {
                auto cur = best[s ^ (1 << i)];
                if (cur.second + w[i] <= x) {
                    cur.second += w[i];
                } else {
                    cur.first++;
                    cur.second = w[i];
                }
                best[s] = min(best[s], cur);
            }
        }
    }
    return n == 0 ? 0 : best[m - 1].first;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll x;
    cin >> n >> x;
    vector<ll> w(n);
    for (ll &v : w) cin >> v;
    cout << minRides(w, x) << '\n';
    return 0;
}

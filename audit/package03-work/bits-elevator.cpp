#include <bits/stdc++.h>
using namespace std;

using ll = long long;

int elevator(const vector<ll>& w, ll x) {
    int n = w.size(), states = 1 << n;
    vector<pair<int, ll>> best(states, {n + 1, 0});
    best[0] = {1, 0};
    for (int s = 1; s < states; s++) {
        for (int p = 0; p < n; p++) {
            if (s & (1 << p)) {
                auto cur = best[s ^ (1 << p)];
                if (cur.second + w[p] <= x) cur.second += w[p];
                else {
                    cur.first++;
                    cur.second = w[p];
                }
                best[s] = min(best[s], cur);
            }
        }
    }
    return n == 0 ? 0 : best[states - 1].first;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll x;
    cin >> n >> x;
    vector<ll> w(n);
    for (ll& v : w) cin >> v;
    cout << elevator(w, x) << '\n';
}

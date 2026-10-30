#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct DivideDP {
    static constexpr ll INF = 1LL << 62;
    int n;
    vector<ll> s, pr, cur;
    DivideDP(int _n) {
        n = _n;
        s.resize(n + 1);
        pr.resize(n + 1);
        cur.resize(n + 1);
    }
    void calc(int l, int r, int ql, int qr) {
        if (l > r) return;
        int mid = l + (r - l) / 2;
        int opt = ql;
        ll best = INF;
        for (int j = ql; j <= min(mid - 1, qr); j++) {
            if (pr[j] == INF) continue;
            ll sum = s[mid] - s[j];
            ll val = pr[j] + sum * sum;
            if (val <= best) {
                best = val;
                opt = j;
            }
        }
        cur[mid] = best;
        calc(l, mid - 1, ql, opt);
        calc(mid + 1, r, opt, qr);
    }
    ll run(int k) {
        fill(pr.begin(), pr.end(), INF);
        pr[0] = 0;
        for (int g = 1; g <= k; g++) {
            fill(cur.begin(), cur.end(), INF);
            calc(g, n, g - 1, n - 1);
            swap(pr, cur);
        }
        return pr[n];
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    DivideDP dp(n);
    for (int i = 1, x; i <= n; i++) {
        cin >> x;
        dp.s[i] = dp.s[i - 1] + x;
    }
    cout << dp.run(k) << '\n';
}

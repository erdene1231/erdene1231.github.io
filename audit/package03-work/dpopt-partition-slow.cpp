#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<ll> s(n + 1);
    for (int i = 1, x; i <= n; i++) {
        cin >> x;
        s[i] = s[i - 1] + x;
    }
    const ll INF = 1LL << 62;
    vector<ll> pr(n + 1, INF), cur(n + 1);
    pr[0] = 0;
    for (int g = 1; g <= k; g++) {
        fill(cur.begin(), cur.end(), INF);
        for (int i = g; i <= n; i++) {
            for (int j = g - 1; j < i; j++) {
                if (pr[j] == INF) continue;
                ll sum = s[i] - s[j];
                cur[i] = min(cur[i], pr[j] + sum * sum);
            }
        }
        swap(pr, cur);
    }
    cout << pr[n] << '\n';
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> coins(k);
    for (int &c : coins) cin >> c;
    vector<int> best(n + 1, n + 1);
    vector<ll> ways(n + 1);
    best[0] = 0;
    ways[0] = 1;
    for (int s = 1; s <= n; s++) {
        for (int c : coins) {
            if (c > s) continue;
            ways[s] += ways[s - c];
            if (best[s - c] != n + 1) best[s] = min(best[s], best[s - c] + 1);
        }
    }
    cout << (best[n] == n + 1 ? -1 : best[n]) << ' ' << ways[n] << '\n';
}

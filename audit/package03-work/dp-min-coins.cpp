#include <bits/stdc++.h>
using namespace std;

const int INF = 1000000000;
vector<int> coins, val;
vector<char> ready;

int naive(int x) {
    if (x < 0) return INF;
    if (x == 0) return 0;
    int best = INF;
    for (int c : coins) best = min(best, naive(x - c) + 1);
    return best;
}

int memo(int x) {
    if (x < 0) return INF;
    if (x == 0) return 0;
    if (ready[x]) return val[x];
    int best = INF;
    for (int c : coins) best = min(best, memo(x - c) + 1);
    ready[x] = true;
    return val[x] = best;
}

pair<int, vector<int>> iterative(int n) {
    vector<int> dp(n + 1, INF), first(n + 1, -1);
    dp[0] = 0;
    for (int x = 1; x <= n; x++) {
        for (int c : coins) {
            if (x >= c && dp[x - c] + 1 < dp[x]) {
                dp[x] = dp[x - c] + 1;
                first[x] = c;
            }
        }
    }
    if (dp[n] == INF) return {-1, {}};
    vector<int> ans;
    for (int x = n; x > 0; x -= first[x]) ans.push_back(first[x]);
    return {dp[n], ans};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int mode, k, n;
    if (!(cin >> mode >> k >> n)) return 0;
    coins.resize(k);
    for (int& c : coins) cin >> c;
    if (mode == 0) {
        int ans = naive(n);
        cout << (ans == INF ? -1 : ans) << '\n';
    } else if (mode == 1) {
        val.resize(n + 1);
        ready.assign(n + 1, false);
        int ans = memo(n);
        cout << (ans == INF ? -1 : ans) << '\n';
    } else {
        auto [best, ans] = iterative(n);
        cout << best << '\n';
        for (int c : ans) cout << c << ' ';
        cout << '\n';
    }
}

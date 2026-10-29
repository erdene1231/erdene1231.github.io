#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> w(n);
    int W = 0;
    for (int &x : w) {
        cin >> x;
        W += x;
    }
    vector<char> dp(W + 1);
    dp[0] = true;
    for (int v : w) {
        for (int x = W; x >= v; x--) dp[x] |= dp[x - v];
    }
    for (int x = 0; x <= W; x++) cout << int(dp[x]) << (x == W ? '\n' : ' ');
}

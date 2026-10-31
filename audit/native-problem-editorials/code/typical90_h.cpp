#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    string s;
    cin >> n >> s;
    const string target = "atcoder";
    const ll mod = 1000000007;
    array<ll, 8> dp{};
    dp[0] = 1;
    for (char c : s) {
        for (int j = 6; j >= 0; --j) {
            if (c == target[j]) {
                dp[j + 1] = (dp[j + 1] + dp[j]) % mod;
            }
        }
    }
    cout << dp[7] << '\n';
}

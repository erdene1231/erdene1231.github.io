#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> cnt(n + 1);
    for (int p = 2; p <= n; ++p) {
        if (cnt[p] != 0) continue;
        for (int x = p; x <= n; x += p) ++cnt[x];
    }
    int ans = 0;
    for (int x = 2; x <= n; ++x) {
        if (cnt[x] >= k) ++ans;
    }
    cout << ans << '\n';
}

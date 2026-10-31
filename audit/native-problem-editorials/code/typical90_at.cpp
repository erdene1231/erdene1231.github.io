#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    array<array<ll, 46>, 3> cnt{};
    for (int group = 0; group < 3; ++group) {
        for (int i = 0; i < n; ++i) {
            int x;
            cin >> x;
            ++cnt[group][x % 46];
        }
    }
    ll ans = 0;
    for (int i = 0; i < 46; ++i) {
        for (int j = 0; j < 46; ++j) {
            int k = (46 - (i + j) % 46) % 46;
            ans += cnt[0][i] * cnt[1][j] * cnt[2][k];
        }
    }
    cout << ans << '\n';
}

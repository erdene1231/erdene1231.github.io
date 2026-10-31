#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    string s;
    cin >> n >> s;
    int lastO = -1, lastX = -1;
    ll ans = 0;
    for (int i = 0; i < n; ++i) {
        if (s[i] == 'o') lastO = i;
        else lastX = i;
        ans += min(lastO, lastX) + 1;
    }
    cout << ans << '\n';
}

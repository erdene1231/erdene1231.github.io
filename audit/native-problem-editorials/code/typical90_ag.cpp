#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int h, w;
    cin >> h >> w;
    int ans;
    if (h == 1 || w == 1) ans = h * w;
    else ans = ((h + 1) / 2) * ((w + 1) / 2);
    cout << ans << '\n';
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll n, a, b, c;
    cin >> n >> a >> b >> c;
    int best = 10000;
    for (int i = 0; i < best && i * a <= n; ++i) {
        ll rem = n - i * a;
        for (int j = 0; i + j < best && j * b <= rem; ++j) {
            ll rest = rem - j * b;
            if (rest % c == 0) {
                ll count = i + j + rest / c;
                best = int(min<ll>(best, count));
            }
        }
    }
    cout << best << '\n';
}

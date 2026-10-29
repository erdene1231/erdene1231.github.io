#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    ll lo[2] = {LLONG_MAX, LLONG_MAX};
    ll hi[2] = {LLONG_MIN, LLONG_MIN};
    int left[2]{}, right[2]{};
    for (int i = 0; i < n; i++) {
        ll x, y;
        cin >> x >> y;
        ll value[2] = {x + y, y - x};
        for (int j = 0; j < 2; j++) {
            if (value[j] < lo[j]) {
                lo[j] = value[j];
                left[j] = i;
            }
            if (value[j] > hi[j]) {
                hi[j] = value[j];
                right[j] = i;
            }
        }
    }
    int j = hi[0] - lo[0] >= hi[1] - lo[1] ? 0 : 1;
    int a = left[j], b = right[j];
    if (a == b && n > 1) b = (a + 1) % n;
    cout << hi[j] - lo[j] << ' ' << a << ' ' << b << '\n';
}

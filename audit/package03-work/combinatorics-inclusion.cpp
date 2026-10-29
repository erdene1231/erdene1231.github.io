#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, u;
    cin >> n >> u; // 1 <= n <= 16; 0 <= u <= 200000
    int size = 1 << n, full = size - 1;
    vector<ll> f(size), inter, sub;
    for (int i = 0; i < u; i++) {
        int mask;
        cin >> mask; // 0 <= mask < 2^n; one distinct universe element
        f[mask]++;
    }
    inter = sub = f;

    for (int bit = 0; bit < n; bit++) {
        for (int mask = 0; mask < size; mask++) {
            if (!(mask >> bit & 1)) inter[mask] += inter[mask | (1 << bit)];
            else sub[mask] += sub[mask ^ (1 << bit)];
        }
    }

    ll uni = 0, common = 0;
    for (int mask = 1; mask < size; mask++) {
        int sign = __builtin_popcount((unsigned)mask) % 2 ? 1 : -1;
        uni += sign * inter[mask];
        ll united = u - sub[full ^ mask];
        common += sign * united;
    }
    cout << uni << ' ' << common << "\n";
}

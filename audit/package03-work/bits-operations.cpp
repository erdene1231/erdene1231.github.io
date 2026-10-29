#include <bits/stdc++.h>
using namespace std;

using ull = unsigned long long;

constexpr int W = numeric_limits<ull>::digits;

int leading(ull x) {
    return x ? __builtin_clzll(x) : W;
}
int trailing(ull x) {
    return x ? __builtin_ctzll(x) : W;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ull x, y;
    int k;
    cin >> x >> y >> k;
    ull bit = 1ULL << k;
    cout << (x & y) << ' ' << (x | y) << ' ' << (x ^ y) << ' ' << ~x << '\n';
    cout << (x << k) << ' ' << (x >> k) << '\n';
    cout << bool(x & bit) << ' ' << (x | bit) << ' ' << (x & ~bit) << ' ' << (x ^ bit) << '\n';
    cout << (x & (x - 1)) << ' ' << (x & -x) << ' ' << (x | (x - 1)) << '\n';
    cout << (x != 0 && (x & (x - 1)) == 0) << '\n';
    cout << leading(x) << ' ' << trailing(x) << ' ' << __builtin_popcountll(x) << ' ' << __builtin_parityll(x) << '\n';
    unsigned int z = 5328;
    cout << __builtin_clz(z) << ' ' << __builtin_ctz(z) << ' ' << __builtin_popcount(z) << ' ' << __builtin_parity(z) << '\n';
}

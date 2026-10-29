#include <bits/stdc++.h>
using namespace std;

void print_bits(uint32_t x) {
    for (int i = 31; i >= 0; i--) cout << ((x >> i) & 1u);
    cout << '\n';
}

int main() {
    int32_t x = -43;
    uint32_t y = static_cast<uint32_t>(x);
    print_bits(43);
    cout << x << ' ' << y << '\n';
    print_bits(y);
    uint32_t top = UINT32_MAX;
    top++;
    cout << top << '\n';
    int mx = INT_MAX;
    cout << mx << ' ' << 1LL + mx << '\n';
}

#include <bits/stdc++.h>
using namespace std;

int main() {
    int32_t x = -43;
    uint32_t y = static_cast<uint32_t>(x);
    cout << bitset<32>(43) << '\n';
    cout << x << ' ' << y << '\n';
    cout << bitset<32>(y) << '\n';
    uint32_t top = UINT32_MAX;
    top++;
    cout << top << '\n';
    int mx = INT_MAX;
    cout << mx << ' ' << 1LL + mx << '\n';
}

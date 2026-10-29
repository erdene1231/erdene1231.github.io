#include <bits/stdc++.h>
using namespace std;
using ll = long long;

void print(ll a, ll b) {
    ll g = gcd(a, b);
    cout << a / g << '/' << b / g << '\n';
}

int main() {
    int n;
    cin >> n;
    ll total = 0, a = 0, b = 0, both = 0, either = 0;
    for (int i = 0; i < n; i++) {
        ll w;
        int mask;
        cin >> w >> mask;
        total += w;
        if (mask & 1) a += w;
        if (mask & 2) b += w;
        if (mask == 3) both += w;
        if (mask != 0) either += w;
    }
    print(a, total);
    print(b, total);
    print(either, total);
    print(both, total);
    if (b == 0) cout << "UNDEFINED\n";
    else print(both, b);
}

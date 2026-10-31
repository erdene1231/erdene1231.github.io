#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll a, b;
    cin >> a >> b;
    const ll limit = 1000000000000000000LL;
    ll x = a / gcd(a, b);
    if (x > limit / b) cout << "Large\n";
    else cout << x * b << '\n';
}

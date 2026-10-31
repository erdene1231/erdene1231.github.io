#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll a, b, c;
    cin >> a >> b >> c;
    ll g = gcd(gcd(a, b), c);
    ll cuts = (a / g - 1) + (b / g - 1) + (c / g - 1);
    cout << cuts << '\n';
}

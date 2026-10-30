#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll euclid(ll a, ll b) {
    a = abs(a);
    b = abs(b);
    while (b) {
        ll r = a % b;
        a = b;
        b = r;
    }
    return a;
}

bool safe_lcm(ll a, ll b, ll &ans) {
    a = abs(a);
    b = abs(b);
    if (a == 0 || b == 0) {
        ans = 0;
        return true;
    }
    ll x = a / euclid(a, b);
    if (x > LLONG_MAX / b) return false;
    ans = x * b;
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        ll a, b, c;
        cin >> a >> b;
        cout << euclid(a, b) << ' ';
        if (safe_lcm(a, b, c)) cout << c << '\n';
        else cout << "OVERFLOW\n";
    }
}

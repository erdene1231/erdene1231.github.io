#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll fib(int n) {
    ll a = 0, b = 1;
    for (int i = 0; i < n; i++) {
        ll c = a + b;
        a = b;
        b = c;
    }
    return a;
}

ll fact(int n) {
    ll x = 1;
    for (int i = 2; i <= n; i++) {
        x *= i;
    }
    return x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n; // 0 <= n <= 90
    cout << fib(n) << "\n";
    if (n <= 20) cout << fact(n) << "\n";
    else cout << "OUT OF RANGE\n";
    return 0;
}

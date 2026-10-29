#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll factorial(int n) {
    if (n == 0) return 1;
    ll x = factorial(n - 1);
    return n * x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    cout << factorial(n) << '\n';
}

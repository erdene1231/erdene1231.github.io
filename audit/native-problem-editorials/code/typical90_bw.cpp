#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    ll n;
    cin >> n;
    int factors = 0;
    for (ll p = 2; p <= n / p; ++p) {
        while (n % p == 0) {
            n /= p;
            ++factors;
        }
    }
    if (n > 1) ++factors;
    int rounds = 0, capacity = 1;
    while (capacity < factors) {
        capacity *= 2;
        ++rounds;
    }
    cout << rounds << '\n';
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll fact_mod(int n, ll m) {
    ll x = 1 % m;
    for (int i = 2; i <= n; i++) {
        x = x * i % m;
    }
    return x;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll m;
    cin >> n >> m;
    cout << fact_mod(n, m) << "\n";
    return 0;
}

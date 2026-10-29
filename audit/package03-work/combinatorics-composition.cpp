#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<ll> compositions(int n) {
    vector<ll> f(n + 1);
    f[0] = 1;
    for (int s = 1; s <= n; s++) {
        for (int k = 1; k <= s; k++) {
            f[s] += f[s - k];
        }
    }
    return f;
}

int main() {
    int n;
    cin >> n; // 0 <= n <= 60
    auto f = compositions(n);
    for (ll x : f) cout << x << ' ';
    cout << "\n";
    cout << (n == 0 ? 1 : (1LL << (n - 1))) << "\n";
}

#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int digits(ll x, int b) {
    int cnt = 0;
    do {
        cnt++;
        x /= b;
    } while (x > 0);
    return cnt;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    ll x;
    int b;
    cin >> x >> b; // x >= 0, b >= 2
    cout << digits(x, b) << "\n";
    return 0;
}

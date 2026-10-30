#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool possible(ll a, ll b) {
    return (a + b) % 3 == 0 && max(a, b) <= 2 * min(a, b);
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    while (q--) {
        ll a, b;
        cin >> a >> b;
        cout << (possible(a, b) ? "YES" : "NO") << '\n';
    }
}

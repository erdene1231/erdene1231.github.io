#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll euclid(ll a, ll b) {
    if (b == 0) return a;
    return euclid(b, a % b);
}

ll lcm(ll a, ll b) {
    return a / euclid(a, b) * b;
}

int main() {
    ll a, b;
    cin >> a >> b; // 1 <= a,b <= 10^9
    cout << euclid(a, b) << ' ' << lcm(a, b) << "\n";
}

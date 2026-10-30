#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll missing(vector<ll> a) {
    sort(a.begin(), a.end());
    ll r = 0;
    for (ll x : a) {
        if (x > r + 1) return r + 1;
        r += x;
    }
    return r + 1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    cout << missing(a) << '\n';
}

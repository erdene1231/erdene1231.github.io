#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> compress(const vector<ll>& a) {
    vector<ll> xs = a;
    sort(xs.begin(), xs.end());
    xs.erase(unique(xs.begin(), xs.end()), xs.end());
    vector<int> c;
    for (ll x : a) {
        c.push_back(lower_bound(xs.begin(), xs.end(), x) - xs.begin() + 1);
    }
    return c;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll& x : a) cin >> x;
    vector<int> c = compress(a);
    for (int i = 0; i < n; i++) cout << c[i] << (i + 1 == n ? '\n' : ' ');
}

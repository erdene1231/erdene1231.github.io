#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<ll> compress(const vector<ll> &a) {
    vector<ll> v = a;
    sort(v.begin(), v.end());
    v.erase(unique(v.begin(), v.end()), v.end());
    return v;
}

int rankOf(const vector<ll> &v, ll x) {
    return lower_bound(v.begin(), v.end(), x) - v.begin();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    vector<ll> v = compress(a);
    cout << v.size() << '\n';
    for (int i = 0; i < n; i++) {
        if (i) cout << ' ';
        cout << rankOf(v, a[i]) + 1;
    }
    cout << '\n';
    return 0;
}

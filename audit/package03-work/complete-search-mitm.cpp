#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<ll> sums(const vector<ll>& a) {
    vector<ll> s = {0};
    for (ll x : a) {
        vector<ll> shifted(s.size()), next(s.size() * 2);
        for (int i = 0; i < (int)s.size(); i++) shifted[i] = s[i] + x;
        merge(s.begin(), s.end(), shifted.begin(), shifted.end(), next.begin());
        s.swap(next);
    }
    return s;
}

bool possible(const vector<ll>& a, ll target) {
    int n = a.size(), mid = n / 2;
    vector<ll> left(a.begin(), a.begin() + mid);
    vector<ll> right(a.begin() + mid, a.end());
    auto s = sums(left), t = sums(right);
    int i = 0, j = (int)t.size() - 1;
    while (i < (int)s.size() && j >= 0) {
        ll value = s[i] + t[j];
        if (value == target) return true;
        if (value < target) i++;
        else j--;
    }
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll target;
    cin >> n >> target;
    vector<ll> a(n);
    for (ll& x : a) cin >> x;
    cout << (possible(a, target) ? "YES" : "NO") << "\n";
    return 0;
}

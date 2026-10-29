#include <bits/stdc++.h>
using namespace std;
using ll = long long;

pair<int, int> two_sum(const vector<pair<int, int>>& a, ll target) {
    int l = 0, r = (int)a.size() - 1;
    while (l < r) {
        ll sum = 1LL * a[l].first + a[r].first;
        if (sum == target) return {a[l].second, a[r].second};
        if (sum < target) l++;
        else r--;
    }
    return {-1, -1};
}

pair<int, int> binary_sum(const vector<pair<int, int>>& a, ll target) {
    int n = a.size();
    for (int i = 0; i < n; i++) {
        ll need = target - a[i].first;
        auto it = lower_bound(a.begin() + i + 1, a.end(), need,
                              [](const pair<int, int>& p, ll x) {
                                  return p.first < x;
                              });
        if (it != a.end() && it->first == need) return {a[i].second, it->second};
    }
    return {-1, -1};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll target;
    if (!(cin >> n >> target)) return 0;
    vector<pair<int, int>> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i].first;
        a[i].second = i + 1;
    }
    sort(a.begin(), a.end());
    auto [l, r] = two_sum(a, target);
    auto [p, q] = binary_sum(a, target);
    cout << l << ' ' << r << '\n';
    cout << p << ' ' << q << '\n';
}

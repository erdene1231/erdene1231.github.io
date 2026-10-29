#include <bits/stdc++.h>
using namespace std;
using ll = long long;

array<int, 3> three_sum(vector<pair<int, int>>& a, ll target) {
    sort(a.begin(), a.end());
    int n = a.size();
    for (int i = 0; i < n; i++) {
        int l = i + 1, r = n - 1;
        while (l < r) {
            ll sum = 1LL * a[i].first + a[l].first + a[r].first;
            if (sum == target) return {a[i].second, a[l].second, a[r].second};
            if (sum < target) l++;
            else r--;
        }
    }
    return {-1, -1, -1};
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
    auto [i, j, k] = three_sum(a, target);
    cout << i << ' ' << j << ' ' << k << '\n';
}

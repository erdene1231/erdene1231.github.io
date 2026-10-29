#include <bits/stdc++.h>
using namespace std;
using ll = long long;

pair<int, int> find_sum(const vector<int>& a, ll target) {
    int n = a.size(), r = 0;
    ll sum = 0;
    for (int l = 0; l < n; l++) {
        while (r < n && sum + a[r] <= target) sum += a[r++];
        if (r > l && sum == target) return {l, r - 1};
        if (r > l) sum -= a[l];
        else r = l + 1;
    }
    return {-1, -1};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    ll target;
    if (!(cin >> n >> target)) return 0;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    auto [l, r] = find_sum(a, target);
    if (l == -1) cout << "IMPOSSIBLE\n";
    else cout << l + 1 << ' ' << r + 1 << '\n';
}

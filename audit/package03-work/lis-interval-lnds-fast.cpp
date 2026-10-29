#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    vector<ll> tail;
    vector<int> pos, par(n, -1);
    for (int i = 0; i < n; i++) {
        int j = upper_bound(tail.begin(), tail.end(), a[i]) - tail.begin();
        if (j > 0) par[i] = pos[j - 1];
        if (j == int(tail.size())) {
            tail.push_back(a[i]);
            pos.push_back(i);
        } else {
            tail[j] = a[i];
            pos[j] = i;
        }
    }
    int best = pos.empty() ? -1 : pos.back();
    vector<int> path;
    for (int i = best; i != -1; i = par[i]) path.push_back(i);
    reverse(path.begin(), path.end());
    cout << path.size() << '\n';
    for (int i : path) cout << i + 1 << ' ';
    cout << '\n';
}

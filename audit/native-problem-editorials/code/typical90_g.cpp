#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> a(n);
    for (int &x : a) {
        cin >> x;
    }
    sort(a.begin(), a.end());

    int q;
    cin >> q;
    while (q--) {
        int b;
        cin >> b;
        auto it = lower_bound(a.begin(), a.end(), b);
        int ans = INT_MAX;
        if (it != a.end()) {
            ans = min(ans, *it - b);
        }
        if (it != a.begin()) {
            ans = min(ans, b - *prev(it));
        }
        cout << ans << '\n';
    }
}

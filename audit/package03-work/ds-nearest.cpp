#include <bits/stdc++.h>
using namespace std;

int nearest(const set<int>& s, int x) {
    auto it = s.lower_bound(x);
    if (it == s.begin()) return *it;
    if (it == s.end()) return *prev(it);
    int hi = *it;
    int lo = *prev(it);
    return 1LL * x - lo < 1LL * hi - x ? lo : hi;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    set<int> s;
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        s.insert(x);
    }
    while (q--) {
        int x;
        cin >> x;
        if (s.empty()) cout << "EMPTY\n";
        else cout << nearest(s, x) << "\n";
    }
    return 0;
}

#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, l, k;
    cin >> n >> l >> k;
    vector<int> a(n);
    for (int &x : a) {
        cin >> x;
    }
    a.push_back(l);

    auto ok = [&](int x) {
        int cnt = 0, last = 0;
        for (int pos : a) {
            if (pos - last >= x) {
                ++cnt;
                last = pos;
            }
        }
        return cnt >= k + 1;
    };

    int lo = 0, hi = l + 1;
    while (hi - lo > 1) {
        int mid = lo + (hi - lo) / 2;
        if (ok(mid)) {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    cout << lo << '\n';
}

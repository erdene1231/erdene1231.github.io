#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k;
    cin >> n >> k;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    map<int, int> freq;
    int l = 0, ans = 0;
    for (int r = 0; r < n; ++r) {
        ++freq[a[r]];
        while (int(freq.size()) > k) {
            auto it = freq.find(a[l]);
            if (--it->second == 0) freq.erase(it);
            ++l;
        }
        ans = max(ans, r - l + 1);
    }
    cout << ans << '\n';
}

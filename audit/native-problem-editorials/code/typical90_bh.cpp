#include <bits/stdc++.h>
using namespace std;

vector<int> lisLengths(const vector<int> &a) {
    vector<int> tail, length(a.size());
    for (int i = 0; i < int(a.size()); ++i) {
        auto it = lower_bound(tail.begin(), tail.end(), a[i]);
        int pos = int(it - tail.begin());
        if (it == tail.end()) tail.push_back(a[i]);
        else *it = a[i];
        length[i] = pos + 1;
    }
    return length;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    auto left = lisLengths(a);
    reverse(a.begin(), a.end());
    auto right = lisLengths(a);
    int ans = 0;
    for (int i = 0; i < n; ++i) ans = max(ans, left[i] + right[n - 1 - i] - 1);
    cout << ans << '\n';
}

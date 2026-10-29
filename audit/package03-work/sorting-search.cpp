#include <bits/stdc++.h>
using namespace std;

int find_bs(const vector<int>& a, int x) {
    int l = 0, r = (int)a.size() - 1;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        if (a[mid] == x) return mid;
        if (a[mid] > x) r = mid - 1;
        else l = mid + 1;
    }
    return -1;
}

int find_jump(const vector<int>& a, int x) {
    int n = a.size();
    if (n == 0 || a[0] > x) return -1;
    int k = 0;
    for (int b = n / 2; b >= 1; b /= 2) {
        while (k + b < n && a[k + b] <= x) k += b;
    }
    return a[k] == x ? k : -1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int& x : a) cin >> x;
    while (q--) {
        int x;
        cin >> x;
        auto range = equal_range(a.begin(), a.end(), x);
        cout << find_bs(a, x) << " " << find_jump(a, x) << " "
             << range.second - range.first << "\n";
    }
    return 0;
}

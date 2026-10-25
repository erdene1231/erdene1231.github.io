#include <bits/stdc++.h>
using namespace std;

int bound_index(const vector<long long>& a, long long x) {
    int l = 0;
    int r = a.size();

    while (l < r) {
        int mid = l + (r - l) / 2;

        if (a[mid] >= x) {
            r = mid;
        } else {
            l = mid + 1;
        }
    }

    return l;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, q;
    cin >> n >> q;
    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    for (int i = 0; i < q; i++) {
        long long x;
        cin >> x;
        cout << bound_index(a, x) << '\n';
    }

    return 0;
}

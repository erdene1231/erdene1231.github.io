#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<ll> a(n);
    ll total = 0;
    for (ll &x : a) {
        cin >> x;
        total += x;
    }
    if (total % 10 != 0) {
        cout << "No\n";
        return 0;
    }
    ll target = total / 10, sum = 0;
    int right = 0;
    for (int left = 0; left < n; ++left) {
        while (right < left + n && sum < target) {
            sum += a[right % n];
            ++right;
        }
        if (sum == target) {
            cout << "Yes\n";
            return 0;
        }
        sum -= a[left];
    }
    cout << "No\n";
}

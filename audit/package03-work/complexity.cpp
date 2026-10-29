#include <bits/stdc++.h>
using namespace std;
using ll = long long;

ll cubic(const vector<int> &a) {
    int n = int(a.size());
    ll best = 0;
    for(int l = 0; l < n; l++) {
        for(int r = l; r < n; r++) {
            ll sum = 0;
            for(int i = l; i <= r; i++) {
                sum += a[i];
            }
            best = max(best, sum);
        }
    }
    return best;
}

ll quadratic(const vector<int> &a) {
    int n = int(a.size());
    ll best = 0;
    for(int l = 0; l < n; l++) {
        ll sum = 0;
        for(int r = l; r < n; r++) {
            sum += a[r];
            best = max(best, sum);
        }
    }
    return best;
}

ll max_sum(const vector<int> &a) {
    ll best = 0, sum = 0;
    for(int x : a) {
        sum = max(ll(x), sum + x);
        best = max(best, sum);
    }
    return best;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<int> a(n);
    for(int &x : a) {
        cin >> x;
    }
    cout << max_sum(a) << '\n';
    return 0;
}

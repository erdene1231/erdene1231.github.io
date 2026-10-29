#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    cin >> n >> k;
    vector<ll> a(n);
    for (ll &x : a) cin >> x;
    if (k < 1 || k > n) {
        cout << "\n\n";
        return 0;
    }
    deque<int> lo, hi;
    vector<ll> mn, mx;
    for (int i = 0; i < n; i++) {
        while (!lo.empty() && lo.front() <= i - k) lo.pop_front();
        while (!hi.empty() && hi.front() <= i - k) hi.pop_front();
        while (!lo.empty() && a[lo.back()] >= a[i]) lo.pop_back();
        while (!hi.empty() && a[hi.back()] <= a[i]) hi.pop_back();
        lo.push_back(i);
        hi.push_back(i);
        if (i >= k - 1) {
            mn.push_back(a[lo.front()]);
            mx.push_back(a[hi.front()]);
        }
    }
    for (int i = 0; i < int(mn.size()); i++) {
        cout << mn[i] << (i + 1 == int(mn.size()) ? '\n' : ' ');
    }
    for (int i = 0; i < int(mx.size()); i++) {
        cout << mx[i] << (i + 1 == int(mx.size()) ? '\n' : ' ');
    }
}

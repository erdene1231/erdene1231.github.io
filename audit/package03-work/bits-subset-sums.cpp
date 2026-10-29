#include <bits/stdc++.h>
using namespace std;

using ll = long long;

vector<ll> subset_sums(vector<ll> sum, int n) {
    int states = 1 << n;
    for (int k = 0; k < n; k++) {
        for (int s = 0; s < states; s++) {
            if (s & (1 << k)) sum[s] += sum[s ^ (1 << k)];
        }
    }
    return sum;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<ll> value(1 << n);
    for (ll& x : value) cin >> x;
    vector<ll> sum = subset_sums(value, n);
    for (int s = 0; s < (1 << n); s++) cout << sum[s] << (s + 1 == (1 << n) ? '\n' : ' ');
}

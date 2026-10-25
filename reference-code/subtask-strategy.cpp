#include <bits/stdc++.h>
using namespace std;

vector<long long> subset_sums(const vector<long long>& a, long long limit) {
    vector<long long> sums = {0};
    for (long long x : a) {
        int size = sums.size();
        for (int i = 0; i < size; i++) {
            if (sums[i] + x <= limit) {
                sums.push_back(sums[i] + x);
            }
        }
    }
    return sums;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    long long limit;
    cin >> n >> limit;
    vector<long long> a(n);
    for (auto& x : a) {
        cin >> x;
    }

    int mid = n / 2;
    vector<long long> left_values(a.begin(), a.begin() + mid);
    vector<long long> right_values(a.begin() + mid, a.end());
    vector<long long> left = subset_sums(left_values, limit);
    vector<long long> right = subset_sums(right_values, limit);
    sort(right.begin(), right.end());

    long long ans = 0;
    for (long long x : left) {
        auto it = upper_bound(right.begin(), right.end(), limit - x);
        if (it != right.begin()) {
            it--;
            ans = max(ans, x + *it);
        }
    }

    cout << ans << '\n';
    return 0;
}

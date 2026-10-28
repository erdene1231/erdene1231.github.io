#include <bits/stdc++.h>
using namespace std;

int first_not_less(const vector<long long>& values, long long target) {
    int left = 0;
    int right = static_cast<int>(values.size());
    while (left < right) {
        int middle = left + (right - left) / 2;
        if (values[middle] < target) {
            left = middle + 1;
        } else {
            right = middle;
        }
    }
    return left;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count, query_count;
    cin >> count >> query_count;
    vector<long long> values(count);
    for (long long& value : values) {
        cin >> value;
    }
    for (int query = 0; query < query_count; ++query) {
        long long target;
        cin >> target;
        int position = first_not_less(values, target);
        bool found = position < count && values[position] == target;
        cout << position << ' ' << found << '\n';
    }
}

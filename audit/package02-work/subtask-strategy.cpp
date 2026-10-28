#include <bits/stdc++.h>
using namespace std;

vector<long long> subset_sums(const vector<long long>& values) {
    vector<long long> sums;
    sums.reserve(size_t{1} << values.size());
    sums.push_back(0);
    for (long long value : values) {
        size_t old_size = sums.size();
        for (size_t index = 0; index < old_size; ++index) {
            sums.push_back(sums[index] + value);
        }
    }
    return sums;
}

long long count_subsets(const vector<long long>& values, long long target) {
    size_t middle = values.size() / 2;
    vector<long long> left_values(values.begin(), values.begin() + middle);
    vector<long long> right_values(values.begin() + middle, values.end());
    vector<long long> left_sums = subset_sums(left_values);
    vector<long long> right_sums = subset_sums(right_values);
    sort(right_sums.begin(), right_sums.end());
    long long answer = 0;
    for (long long left_sum : left_sums) {
        auto [first, last] = equal_range(right_sums.begin(), right_sums.end(), target - left_sum);
        answer += static_cast<long long>(last - first);
    }
    return answer;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count;
    long long target;
    cin >> count >> target;
    vector<long long> values(count);
    for (long long& value : values) {
        cin >> value;
    }
    cout << count_subsets(values, target) << '\n';
}

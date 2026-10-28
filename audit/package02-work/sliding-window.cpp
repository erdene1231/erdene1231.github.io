#include <iostream>
#include <vector>
using namespace std;

long long count_target_windows(const vector<long long>& values, long long target) {
    int left = 0;
    long long sum = 0;
    long long answer = 0;

    for (int right = 0; right < static_cast<int>(values.size()); ++right) {
        sum += values[right];
        while (left <= right && sum > target) {
            sum -= values[left];
            ++left;
        }
        if (sum == target) {
            ++answer;
        }
    }
    return answer;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int size;
    long long target;
    cin >> size >> target;
    vector<long long> values(size);
    for (long long& value : values) {
        cin >> value;
    }
    cout << count_target_windows(values, target) << '\n';
    return 0;
}

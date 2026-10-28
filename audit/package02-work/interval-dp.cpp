#include <bits/stdc++.h>
using namespace std;

long long minimum_merge_cost(const vector<long long>& values) {
    int count = static_cast<int>(values.size());
    if (count == 0) {
        return 0;
    }
    vector<long long> prefix(count + 1);
    for (int index = 0; index < count; ++index) {
        prefix[index + 1] = prefix[index] + values[index];
    }
    vector<vector<long long>> cost(count, vector<long long>(count));
    for (int length = 2; length <= count; ++length) {
        for (int left = 0; left + length <= count; ++left) {
            int right = left + length - 1;
            long long best = numeric_limits<long long>::max();
            long long sum = prefix[right + 1] - prefix[left];
            for (int split = left; split < right; ++split) {
                best = min(best, cost[left][split] + cost[split + 1][right] + sum);
            }
            cost[left][right] = best;
        }
    }
    return cost[0][count - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count;
    cin >> count;
    vector<long long> values(count);
    for (long long& value : values) {
        cin >> value;
    }
    cout << minimum_merge_cost(values) << '\n';
}

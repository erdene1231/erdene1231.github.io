#include <bits/stdc++.h>
using namespace std;

long long best_value(const vector<int>& weight, const vector<int>& value, int capacity) {
    vector<long long> best(capacity + 1);
    for (int item = 0; item < static_cast<int>(weight.size()); ++item) {
        for (int limit = capacity; limit >= weight[item]; --limit) {
            best[limit] = max(best[limit], best[limit - weight[item]] + value[item]);
        }
    }
    return best[capacity];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int item_count, capacity;
    cin >> item_count >> capacity;
    vector<int> weight(item_count), value(item_count);
    for (int item = 0; item < item_count; ++item) {
        cin >> weight[item] >> value[item];
    }
    cout << best_value(weight, value, capacity) << '\n';
}

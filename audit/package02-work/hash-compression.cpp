#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

struct Compression {
    vector<long long> values;
    vector<int> ranks;
};

Compression compress(const vector<long long>& input) {
    vector<long long> values = input;
    sort(values.begin(), values.end());
    values.erase(unique(values.begin(), values.end()), values.end());

    vector<int> ranks;
    ranks.reserve(input.size());
    for (long long value : input) {
        auto position = lower_bound(values.begin(), values.end(), value);
        ranks.push_back(static_cast<int>(position - values.begin()) + 1);
    }
    return {values, ranks};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int value_count;
    cin >> value_count;
    vector<long long> input(value_count);
    for (long long& value : input) {
        cin >> value;
    }

    Compression result = compress(input);
    cout << result.values.size() << '\n';
    for (long long value : result.values) {
        cout << value << ' ';
    }
    cout << '\n';
    for (int rank : result.ranks) {
        cout << rank << ' ';
    }
    cout << '\n';
    return 0;
}

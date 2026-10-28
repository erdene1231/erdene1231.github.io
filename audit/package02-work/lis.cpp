#include <bits/stdc++.h>
using namespace std;

int increasing_length(const vector<long long>& values) {
    vector<long long> tails;
    for (long long value : values) {
        auto position = lower_bound(tails.begin(), tails.end(), value);
        if (position == tails.end()) {
            tails.push_back(value);
        } else {
            *position = value;
        }
    }
    return static_cast<int>(tails.size());
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
    cout << increasing_length(values) << '\n';
}

#include <bits/stdc++.h>
using namespace std;

vector<int> nearest_smaller_left(const vector<long long>& values) {
    vector<int> previous(values.size(), 0);
    vector<int> candidates;
    for (int index = 0; index < static_cast<int>(values.size()); ++index) {
        while (!candidates.empty() && values[candidates.back()] >= values[index]) {
            candidates.pop_back();
        }
        if (!candidates.empty()) {
            previous[index] = candidates.back() + 1;
        }
        candidates.push_back(index);
    }
    return previous;
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
    vector<int> previous = nearest_smaller_left(values);
    for (int index = 0; index < count; ++index) {
        if (index > 0) {
            cout << ' ';
        }
        cout << previous[index];
    }
    cout << '\n';
}

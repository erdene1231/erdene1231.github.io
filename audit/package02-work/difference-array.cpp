#include <iostream>
#include <vector>
using namespace std;

vector<long long> build_difference(const vector<long long>& values) {
    int size = static_cast<int>(values.size());
    vector<long long> difference(size + 1, 0);
    for (int index = 0; index < size; ++index) {
        difference[index] += values[index];
        difference[index + 1] -= values[index];
    }
    return difference;
}

void add_range(vector<long long>& difference, int left, int right,
               long long amount) {
    difference[left] += amount;
    difference[right] -= amount;
}

vector<long long> restore_values(const vector<long long>& difference) {
    int size = static_cast<int>(difference.size()) - 1;
    vector<long long> values(size);
    long long current = 0;
    for (int index = 0; index < size; ++index) {
        current += difference[index];
        values[index] = current;
    }
    return values;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int size, update_count;
    cin >> size >> update_count;
    vector<long long> values(size);
    for (long long& value : values) {
        cin >> value;
    }
    vector<long long> difference = build_difference(values);
    for (int update = 0; update < update_count; ++update) {
        int left, right;
        long long amount;
        cin >> left >> right >> amount;
        add_range(difference, left - 1, right, amount);
    }
    values = restore_values(difference);
    for (int index = 0; index < size; ++index) {
        if (index > 0) {
            cout << ' ';
        }
        cout << values[index];
    }
    cout << '\n';
    return 0;
}

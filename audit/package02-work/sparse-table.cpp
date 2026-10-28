#include <bits/stdc++.h>
using namespace std;

class SparseMinimum {
    vector<int> logarithm;
    vector<vector<long long>> table;
public:
    explicit SparseMinimum(const vector<long long>& values) {
        int count = static_cast<int>(values.size());
        logarithm.resize(count + 1);
        for (int length = 2; length <= count; ++length) {
            logarithm[length] = logarithm[length / 2] + 1;
        }
        int levels = logarithm[count] + 1;
        table.assign(levels, vector<long long>(count));
        table[0] = values;
        for (int level = 1; level < levels; ++level) {
            int half = 1 << (level - 1);
            for (int left = 0; left + 2 * half <= count; ++left) {
                table[level][left] = min(table[level - 1][left],
                                         table[level - 1][left + half]);
            }
        }
    }
    long long range_minimum(int left, int right) const {
        int level = logarithm[right - left + 1];
        int length = 1 << level;
        return min(table[level][left], table[level][right - length + 1]);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count, query_count;
    cin >> count >> query_count;
    vector<long long> values(count);
    for (long long& value : values) {
        cin >> value;
    }
    SparseMinimum table(values);
    for (int query = 0; query < query_count; ++query) {
        int left, right;
        cin >> left >> right;
        cout << table.range_minimum(left - 1, right - 1) << '\n';
    }
}

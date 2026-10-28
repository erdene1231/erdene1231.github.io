#include <iostream>
#include <vector>
using namespace std;

using Grid = vector<vector<long long>>;

Grid build_prefix(const Grid& values, int columns) {
    int rows = static_cast<int>(values.size());
    Grid prefix(rows + 1, vector<long long>(columns + 1, 0));
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            prefix[row + 1][column + 1] = values[row][column]
                + prefix[row][column + 1] + prefix[row + 1][column]
                - prefix[row][column];
        }
    }
    return prefix;
}

long long rectangle_sum(const Grid& prefix, int top, int left,
                        int bottom, int right) {
    return prefix[bottom][right] - prefix[top][right]
        - prefix[bottom][left] + prefix[top][left];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int rows, columns, query_count;
    cin >> rows >> columns >> query_count;
    Grid values(rows, vector<long long>(columns));
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            cin >> values[row][column];
        }
    }
    Grid prefix = build_prefix(values, columns);

    for (int query = 0; query < query_count; ++query) {
        int top, left, bottom, right;
        cin >> top >> left >> bottom >> right;
        cout << rectangle_sum(prefix, top - 1, left - 1, bottom, right) << '\n';
    }
    return 0;
}

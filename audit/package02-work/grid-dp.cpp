#include <bits/stdc++.h>
using namespace std;

constexpr int MOD = 1000000007;

int count_paths(const vector<string>& grid) {
    int rows = static_cast<int>(grid.size());
    int columns = static_cast<int>(grid[0].size());
    vector<vector<int>> ways(rows, vector<int>(columns));
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            if (grid[row][column] == '#') {
                continue;
            }
            if (row == 0 && column == 0) {
                ways[row][column] = 1;
                continue;
            }
            int from_above = row > 0 ? ways[row - 1][column] : 0;
            int from_left = column > 0 ? ways[row][column - 1] : 0;
            ways[row][column] = (from_above + from_left) % MOD;
        }
    }
    return ways[rows - 1][columns - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int rows, columns;
    cin >> rows >> columns;
    vector<string> grid(rows);
    for (string& line : grid) {
        cin >> line;
    }
    cout << count_paths(grid) << '\n';
}

#include <iostream>
#include <queue>
#include <string>
#include <utility>
#include <vector>
using namespace std;

struct Region {
    int area = 0;
    int perimeter = 0;
};

Region explore_region(const vector<string>& grid,
                      vector<vector<bool>>& visited,
                      int start_row, int start_column) {
    int rows = static_cast<int>(grid.size());
    int columns = static_cast<int>(grid[0].size());
    const int row_step[4] = {-1, 1, 0, 0};
    const int column_step[4] = {0, 0, -1, 1};
    queue<pair<int, int>> pending;
    visited[start_row][start_column] = true;
    pending.push({start_row, start_column});
    Region region;

    while (!pending.empty()) {
        int row = pending.front().first;
        int column = pending.front().second;
        pending.pop();
        ++region.area;
        for (int direction = 0; direction < 4; ++direction) {
            int next_row = row + row_step[direction];
            int next_column = column + column_step[direction];
            if (next_row < 0 || next_row >= rows ||
                next_column < 0 || next_column >= columns) {
                ++region.perimeter;
                continue;
            }
            if (grid[next_row][next_column] == '#') {
                ++region.perimeter;
                continue;
            }
            if (!visited[next_row][next_column]) {
                visited[next_row][next_column] = true;
                pending.push({next_row, next_column});
            }
        }
    }
    return region;
}

vector<Region> find_regions(const vector<string>& grid) {
    int rows = static_cast<int>(grid.size());
    int columns = static_cast<int>(grid[0].size());
    vector<vector<bool>> visited(rows, vector<bool>(columns, false));
    vector<Region> regions;
    for (int row = 0; row < rows; ++row) {
        for (int column = 0; column < columns; ++column) {
            if (grid[row][column] == '.' && !visited[row][column]) {
                regions.push_back(explore_region(grid, visited, row, column));
            }
        }
    }
    return regions;
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

    vector<Region> regions = find_regions(grid);
    cout << regions.size() << '\n';
    for (const Region& region : regions) {
        cout << region.area << ' ' << region.perimeter << '\n';
    }
    return 0;
}

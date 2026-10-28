#include <bits/stdc++.h>
using namespace std;

constexpr int MOD = 1000000007;

int count_assignments(const vector<vector<int>>& allowed) {
    int count = static_cast<int>(allowed.size());
    int state_count = 1 << count;
    vector<int> used_count(state_count), ways(state_count);
    for (int mask = 1; mask < state_count; ++mask) {
        used_count[mask] = used_count[mask >> 1] + (mask & 1);
    }
    ways[0] = 1;
    for (int mask = 0; mask < state_count; ++mask) {
        int person = used_count[mask];
        if (person == count || ways[mask] == 0) {
            continue;
        }
        for (int option = 0; option < count; ++option) {
            if ((mask & (1 << option)) == 0 && allowed[person][option]) {
                int& next = ways[mask | (1 << option)];
                next += ways[mask];
                if (next >= MOD) {
                    next -= MOD;
                }
            }
        }
    }
    return ways[state_count - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count;
    cin >> count;
    vector<vector<int>> allowed(count, vector<int>(count));
    for (auto& row : allowed) {
        for (int& value : row) {
            cin >> value;
        }
    }
    cout << count_assignments(allowed) << '\n';
}

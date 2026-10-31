#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<vector<int>> sum(n + 1, vector<int>(n + 1));
    for (int i = 1; i <= n; ++i) {
        for (int j = 1; j <= n; ++j) {
            int x;
            cin >> x;
            sum[i][j] = x + sum[i - 1][j] + sum[i][j - 1] - sum[i - 1][j - 1];
        }
    }
    vector<int> best(n * n + 1);
    for (int top = 0; top < n; ++top) {
        for (int bottom = top + 1; bottom <= n; ++bottom) {
            for (int left = 0; left < n; ++left) {
                for (int right = left + 1; right <= n; ++right) {
                    int area = (bottom - top) * (right - left);
                    int value = sum[bottom][right] - sum[top][right] - sum[bottom][left] + sum[top][left];
                    best[area] = max(best[area], value);
                }
            }
        }
    }
    for (int area = 1; area <= n * n; ++area) best[area] = max(best[area], best[area - 1]);
    int q;
    cin >> q;
    while (q--) {
        int p;
        cin >> p;
        cout << best[p] << '\n';
    }
}

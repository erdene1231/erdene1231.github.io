#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, k, maxA = 0, maxB = 0;
    cin >> n >> k;
    vector<pair<int, int>> points(n);
    for (auto &[a, b] : points) {
        cin >> a >> b;
        maxA = max(maxA, a);
        maxB = max(maxB, b);
    }
    vector<vector<int>> sum(maxA + 1, vector<int>(maxB + 1));
    for (auto [a, b] : points) ++sum[a][b];
    for (int a = 1; a <= maxA; ++a) {
        for (int b = 1; b <= maxB; ++b) {
            sum[a][b] += sum[a - 1][b] + sum[a][b - 1] - sum[a - 1][b - 1];
        }
    }
    int ans = 0;
    for (int a = 1; a <= maxA; ++a) {
        for (int b = 1; b <= maxB; ++b) {
            int right = min(maxA, a + k), top = min(maxB, b + k);
            int count = sum[right][top] - sum[a - 1][top] - sum[right][b - 1] + sum[a - 1][b - 1];
            ans = max(ans, count);
        }
    }
    cout << ans << '\n';
}

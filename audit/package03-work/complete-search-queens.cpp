#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> col, diag1, diag2;
int search(int row) {
    if (row == n) return 1;
    int ans = 0;
    for (int x = 0; x < n; x++) {
        int d1 = x + row, d2 = x - row + n - 1;
        if (col[x] || diag1[d1] || diag2[d2]) continue;
        col[x] = diag1[d1] = diag2[d2] = 1;
        ans += search(row + 1);
        col[x] = diag1[d1] = diag2[d2] = 0;
    }
    return ans;
}

int main() {
    cin >> n; // 1 <= n <= 14 for this runnable demonstration.
    col.assign(n, 0);
    diag1.assign(2 * n - 1, 0);
    diag2.assign(2 * n - 1, 0);
    cout << search(0) << "\n";
    return 0;
}

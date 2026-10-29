#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> solve(int n) {
    vector<int> take(n + 1);
    for (int k = 2; k <= n; k++) {
        for (int d = 1; d <= k / d; d++) {
            if (k % d != 0) continue;
            int e = k / d;
            if (d < k && take[k - d] == 0) take[k] = d;
            if (e < k && take[k - e] == 0) take[k] = e;
        }
    }
    return take;
}

int main() {
    int n;
    cin >> n;
    auto take = solve(n);
    cout << (take[n] ? "WIN" : "LOSE") << ' ' << take[n] << '\n';
    for (int k = 1; k <= n; k++) cout << (take[k] ? 'W' : 'L');
    cout << '\n';
}

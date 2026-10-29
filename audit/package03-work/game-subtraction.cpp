#include <bits/stdc++.h>
using namespace std;
using ll = long long;

vector<int> solve(int n, const vector<int> &a) {
    vector<int> take(n + 1);
    for (int k = 1; k <= n; k++) {
        for (int x : a) {
            if (x <= k && take[k - x] == 0) {
                take[k] = x;
                break;
            }
        }
    }
    return take;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<int> a(m);
    for (int &x : a) cin >> x;
    auto take = solve(n, a);
    cout << (take[n] ? "WIN" : "LOSE") << ' ' << take[n] << '\n';
    for (int k = 0; k <= n; k++) cout << (take[k] ? 'W' : 'L');
    cout << '\n';
}

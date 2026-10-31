#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int nextState(int x) {
    int sum = 0;
    for (int t = x; t > 0; t /= 10) sum += t % 10;
    return (x + sum) % 100000;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll k;
    cin >> n >> k;
    vector<int> seen(100000, -1), path;
    int cur = n;
    while (seen[cur] == -1) {
        seen[cur] = int(path.size());
        path.push_back(cur);
        cur = nextState(cur);
    }
    ll at = k;
    if (k >= ll(path.size())) {
        int start = seen[cur];
        int length = int(path.size()) - start;
        at = start + (k - start) % length;
    }
    cout << path[int(at)] << '\n';
}

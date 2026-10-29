#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int k;
    cin >> k;
    vector<int> a(k);
    int n = 0;
    for (int &x : a) {
        cin >> x;
        n += x;
    }
    vector<int> count(n + 1), rem(n + 1, -1);
    for (int x : a) count[x]++;
    rem[0] = 0;
    for (int w = 1; w <= n; w++) {
        if (!count[w]) continue;
        for (int s = 0; s <= n; s++) {
            if (rem[s] >= 0) rem[s] = count[w];
            else if (s < w || rem[s - w] <= 0) rem[s] = -1;
            else rem[s] = rem[s - w] - 1;
        }
    }
    for (int s = 0; s <= n; s++) {
        if (rem[s] >= 0) cout << s << ' ';
    }
    cout << '\n';
}

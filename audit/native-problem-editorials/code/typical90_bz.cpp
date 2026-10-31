#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, m;
    cin >> n >> m;
    vector<int> smaller(n + 1);
    while (m--) {
        int a, b;
        cin >> a >> b;
        ++smaller[max(a, b)];
    }
    cout << count(smaller.begin() + 1, smaller.end(), 1) << '\n';
}

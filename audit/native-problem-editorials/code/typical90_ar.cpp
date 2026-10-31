#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n, q;
    cin >> n >> q;
    vector<int> a(n);
    for (int &x : a) cin >> x;
    int head = 0;
    while (q--) {
        int type, x, y;
        cin >> type >> x >> y;
        if (type == 1) swap(a[(head + x - 1) % n], a[(head + y - 1) % n]);
        else if (type == 2) head = (head + n - 1) % n;
        else cout << a[(head + x - 1) % n] << '\n';
    }
}

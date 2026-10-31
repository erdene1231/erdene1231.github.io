#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q;
    cin >> q;
    deque<int> d;
    while (q--) {
        int type, x;
        cin >> type >> x;
        if (type == 1) d.push_front(x);
        else if (type == 2) d.push_back(x);
        else cout << d[x - 1] << '\n';
    }
}

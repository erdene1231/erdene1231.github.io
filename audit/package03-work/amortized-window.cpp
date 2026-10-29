#include <bits/stdc++.h>
using namespace std;

struct MinQueue {
    int k;
    deque<pair<int, int>> q;

    MinQueue(int _k) {
        k = _k;
    }

    void add(int i, int x) {
        while (!q.empty() && q.front().second <= i - k) q.pop_front();
        while (!q.empty() && q.back().first >= x) q.pop_back();
        q.push_back({x, i});
    }

    int minimum() const {
        return q.front().first;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, k;
    if (!(cin >> n >> k)) return 0;
    MinQueue window(k);
    for (int i = 0; i < n; i++) {
        int x;
        cin >> x;
        window.add(i, x);
        if (i >= k - 1) cout << window.minimum() << ' ';
    }
    cout << '\n';
}

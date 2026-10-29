#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Task {
    int a, d, id;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<Task> t(n);
    for (int i = 0; i < n; i++) {
        cin >> t[i].a >> t[i].d;
        t[i].id = i + 1;
    }
    sort(t.begin(), t.end(), [](const Task& x, const Task& y) {
        return tie(x.a, x.id) < tie(y.a, y.id);
    });
    ll time = 0, ans = 0;
    for (auto task : t) {
        time += task.a;
        ans += task.d - time;
    }
    cout << ans << '\n';
    for (auto task : t) cout << task.id << ' ';
    cout << '\n';
}

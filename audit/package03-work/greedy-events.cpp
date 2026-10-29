#include <bits/stdc++.h>
using namespace std;

struct Event {
    int l, r, id;
};

vector<int> choose(vector<Event>& a) {
    sort(a.begin(), a.end(), [](const Event& x, const Event& y) {
        return tie(x.r, x.l, x.id) < tie(y.r, y.l, y.id);
    });
    vector<int> ans;
    int last = -1;
    for (auto e : a) {
        if (e.l < last) continue;
        ans.push_back(e.id);
        last = e.r;
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<Event> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i].l >> a[i].r;
        a[i].id = i + 1;
    }
    vector<int> ans = choose(a);
    cout << ans.size() << '\n';
    for (int id : ans) cout << id << ' ';
    cout << '\n';
}

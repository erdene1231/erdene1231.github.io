#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Stay {
    ll l, r;
    int id;
    bool operator<(const Stay &s) const {
        return tie(l, r, id) < tie(s.l, s.r, s.id);
    }
};

pair<int, vector<int>> allocate(vector<Stay> a) {
    sort(a.begin(), a.end());
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> q;
    vector<int> ans(a.size());
    int rooms = 0;
    for (Stay s : a) {
        int id;
        if (!q.empty() && q.top().first < s.l) {
            id = q.top().second;
            q.pop();
        } else id = ++rooms;
        ans[s.id] = id;
        q.push({s.r, id});
    }
    return {rooms, ans};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<Stay> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i].l >> a[i].r;
        a[i].id = i;
    }
    auto [rooms, ans] = allocate(a);
    cout << rooms << '\n';
    for (int id : ans) cout << id << ' ';
    cout << '\n';
}

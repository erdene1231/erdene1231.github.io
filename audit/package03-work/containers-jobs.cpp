#include <bits/stdc++.h>
using namespace std;
using ll = long long;

struct Job {
    ll p;
    int id;
};

struct Cmp {
    bool operator()(const Job &a, const Job &b) const {
        if (a.p != b.p) return a.p < b.p;
        return a.id > b.id;
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    priority_queue<Job, vector<Job>, Cmp> q;
    for (int i = 1; i <= n; i++) {
        ll p;
        cin >> p;
        q.push({p, i});
    }
    while (!q.empty()) {
        Job cur = q.top();
        q.pop();
        cout << cur.id << ' ' << cur.p << '\n';
    }
}

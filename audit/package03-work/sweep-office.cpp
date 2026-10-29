#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    vector<pair<ll, int>> events;
    for (int i = 0; i < n; i++) {
        ll a, b;
        cin >> a >> b;
        if (a == b) continue;
        events.push_back({a, 1});
        events.push_back({b, -1});
    }
    sort(events.begin(), events.end());
    int active = 0, best = 0;
    for (int i = 0; i < (int) events.size();) {
        ll time = events[i].first;
        while (i < (int) events.size() && events[i].first == time) {
            active += events[i].second;
            i++;
        }
        best = max(best, active);
    }
    cout << best << '\n';
}

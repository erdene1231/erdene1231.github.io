#include <bits/stdc++.h>
using namespace std;
using ll = long long;

pair<int, ll> absolute_sum(vector<int> a) {
    sort(a.begin(), a.end());
    int x = a[a.size() / 2];
    ll cost = 0;
    for (int v : a) cost += abs(1LL * v - x);
    return {x, cost};
}

pair<long double, long double> square_sum(const vector<int>& a) {
    ll sum = 0;
    for (int v : a) sum += v;
    long double x = (long double)sum / a.size();
    long double cost = 0;
    for (int v : a) {
        long double d = v - x;
        cost += d * d;
    }
    return {x, cost};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int& v : a) cin >> v;
    auto [median, first] = absolute_sum(a);
    auto [mean, second] = square_sum(a);
    cout << median << ' ' << first << '\n';
    cout << fixed << setprecision(10) << mean << ' ' << second << '\n';
}

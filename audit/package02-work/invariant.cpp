#include <bits/stdc++.h>
using namespace std;

long long smallest_missing_sum(vector<long long> coins) {
    sort(coins.begin(), coins.end());
    long long reachable = 0;
    for (long long coin : coins) {
        if (coin > reachable + 1) {
            break;
        }
        reachable += coin;
    }
    return reachable + 1;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count;
    cin >> count;
    vector<long long> coins(count);
    for (long long& coin : coins) {
        cin >> coin;
    }
    cout << smallest_missing_sum(coins) << '\n';
}

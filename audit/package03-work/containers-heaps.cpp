#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    priority_queue<ll> hi;
    priority_queue<ll, vector<ll>, greater<ll>> lo;
    while (n--) {
        string cmd;
        cin >> cmd;
        if (cmd == "PUSH") {
            ll x;
            cin >> x;
            hi.push(x);
            lo.push(x);
        } else if (cmd == "PEEK") {
            if (hi.empty()) cout << "EMPTY\n";
            else cout << hi.top() << ' ' << lo.top() << '\n';
        } else if (cmd == "POP") {
            if (hi.empty()) cout << "EMPTY\n";
            else {
                cout << hi.top() << ' ' << lo.top() << '\n';
                hi.pop();
                lo.pop();
            }
        } else if (cmd == "SIZE") cout << hi.size() << '\n';
    }
}

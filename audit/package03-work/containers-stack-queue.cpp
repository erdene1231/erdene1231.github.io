#include <bits/stdc++.h>
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    stack<ll> s;
    queue<ll> q;
    while (n--) {
        string cmd;
        cin >> cmd;
        if (cmd == "PUSH") {
            ll x;
            cin >> x;
            s.push(x);
            q.push(x);
        } else if (cmd == "PEEK") {
            if (s.empty()) cout << "EMPTY\n";
            else cout << s.top() << ' ' << q.front() << ' ' << q.back() << '\n';
        } else if (cmd == "POP") {
            if (s.empty()) cout << "EMPTY\n";
            else {
                cout << s.top() << ' ' << q.front() << '\n';
                s.pop();
                q.pop();
            }
        } else if (cmd == "SIZE") {
            cout << s.size() << '\n';
        }
    }
}

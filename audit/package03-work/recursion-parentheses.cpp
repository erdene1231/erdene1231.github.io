#include <bits/stdc++.h>
using namespace std;

void generate(int open, int close, int n, string &cur) {
    if (open == n && close == n) {
        cout << cur << '\n';
        return;
    }
    if (open < n) {
        cur.push_back('(');
        generate(open + 1, close, n, cur);
        cur.pop_back();
    }
    if (close < open) {
        cur.push_back(')');
        generate(open, close + 1, n, cur);
        cur.pop_back();
    }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    string cur;
    cur.reserve(2 * n);
    generate(0, 0, n, cur);
}

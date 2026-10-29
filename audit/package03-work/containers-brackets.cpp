#include <bits/stdc++.h>
using namespace std;
using ll = long long;

bool match(char a, char b) {
    return (a == '(' && b == ')') || (a == '[' && b == ']') ||
           (a == '{' && b == '}');
}

bool balanced(const string &s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') st.push(c);
        else {
            if (st.empty() || !match(st.top(), c)) return false;
            st.pop();
        }
    }
    return st.empty();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    string s;
    getline(cin, s);
    cout << (balanced(s) ? "YES" : "NO") << '\n';
}

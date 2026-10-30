#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n) || n < 1 || n > 1000000000) return 1;
    int l = 1, r = n;
    while (l <= r) {
        int mid = l + (r - l) / 2;
        cout << "? " << mid << endl;
        string s;
        if (!(cin >> s) || s == "-1") return 1;
        if (s == "=") {
            cout << "! " << mid << endl;
            if (!(cin >> s) || s != "OK") return 1;
            return 0;
        }
        if (s == "<") r = mid - 1;
        else if (s == ">") l = mid + 1;
        else return 1;
    }
    return 1;
}

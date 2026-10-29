#include <bits/stdc++.h>
using namespace std;

int n;
vector<int> subset;
void print_subset() {
    cout << "{";
    for (int i = 0; i < (int)subset.size(); i++) {
        if (i) cout << " ";
        cout << subset[i];
    }
    cout << "}\n";
}
void search(int k) {
    if (k == n) {
        print_subset();
        return;
    }
    search(k + 1);
    subset.push_back(k);
    search(k + 1);
    subset.pop_back();
}
int main() {
    cin >> n; // 0 <= n <= 20; output itself is exponential.
    cout << "REC\n";
    search(0);
    cout << "MASK\n";
    for (int b = 0; b < (1 << n); b++) {
        subset.clear();
        for (int i = 0; i < n; i++) {
            if (b & (1 << i)) subset.push_back(i);
        }
        print_subset();
    }
    return 0;
}

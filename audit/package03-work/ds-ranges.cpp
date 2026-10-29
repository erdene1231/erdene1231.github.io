#include <bits/stdc++.h>
using namespace std;

int main() {
    vector<int> v = {3, 4, 6, 8, 12, 13, 14, 17};
    sort(v.begin(), v.end());
    reverse(v.begin(), v.end());
    mt19937 rng(123456789);
    shuffle(v.begin(), v.end(), rng);
    for (int x : v) cout << x << " ";
    cout << "\n";
    int a[] = {3, 4, 6, 8, 12, 13, 14, 17};
    int n = 8;
    sort(a, a + n);
    reverse(a, a + n);
    shuffle(a, a + n, rng);
    for (int x : a) cout << x << " ";
    cout << "\n";
    return 0;
}

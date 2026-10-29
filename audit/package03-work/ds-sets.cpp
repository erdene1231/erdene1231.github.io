#include <bits/stdc++.h>
using namespace std;

int main() {
    set<int> s;
    s.insert(3);
    s.insert(2);
    s.insert(5);
    cout << s.count(3) << " " << s.count(4) << "\n";
    s.erase(3);
    s.insert(4);
    cout << s.count(3) << " " << s.count(4) << "\n";
    set<int> a = {2, 5, 6, 8};
    cout << a.size() << "\n";
    for (int x : a) cout << x << " ";
    cout << "\n";
    set<int> one;
    one.insert(5);
    one.insert(5);
    one.insert(5);
    cout << one.count(5) << "\n";
    multiset<int> ms = {5, 5, 5};
    cout << ms.count(5) << "\n";
    auto it = ms.find(5);
    if (it != ms.end()) ms.erase(it);
    cout << ms.count(5) << "\n";
    ms.erase(5);
    cout << ms.count(5) << "\n";
    return 0;
}

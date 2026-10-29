#include <bits/stdc++.h>
#include <ext/pb_ds/assoc_container.hpp>
#include <ext/pb_ds/tree_policy.hpp>
using namespace std;
using namespace __gnu_pbds;

using indexed_set = tree<int, null_type, less<int>, rb_tree_tag,
                         tree_order_statistics_node_update>;

int main() {
    indexed_set s;
    for (int x : {2, 3, 7, 9}) s.insert(x);
    auto it = s.find_by_order(2);
    if (it != s.end()) cout << *it << "\n";
    cout << s.order_of_key(7) << "\n";
    cout << s.order_of_key(6) << "\n";
    cout << s.order_of_key(8) << "\n";
    return 0;
}

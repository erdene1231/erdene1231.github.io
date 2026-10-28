#include <iostream>
#include <map>
#include <set>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int value_count, query_count;
    cin >> value_count >> query_count;
    set<long long> distinct;
    map<long long, int> frequency;

    for (int index = 0; index < value_count; ++index) {
        long long value;
        cin >> value;
        distinct.insert(value);
        ++frequency[value];
    }

    for (int query = 0; query < query_count; ++query) {
        long long value;
        cin >> value;
        auto found = frequency.find(value);
        int count = (found == frequency.end() ? 0 : found->second);
        cout << count << '\n';
    }

    cout << distinct.size() << '\n';
    for (long long value : distinct) {
        cout << value << ' ' << frequency.at(value) << '\n';
    }
    return 0;
}

#include <bits/stdc++.h>
using namespace std;

class Fenwick {
    int count;
    vector<long long> tree;
public:
    explicit Fenwick(int size) : count(size), tree(size + 1) {}
    void add(int position, long long change) {
        for (int index = position; index <= count; index += index & -index) {
            tree[index] += change;
        }
    }
    long long prefix_sum(int position) const {
        long long total = 0;
        for (int index = position; index > 0; index -= index & -index) {
            total += tree[index];
        }
        return total;
    }
    long long range_sum(int left, int right) const {
        return prefix_sum(right) - prefix_sum(left - 1);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count, query_count;
    cin >> count >> query_count;
    vector<long long> values(count + 1);
    Fenwick tree(count);
    for (int index = 1; index <= count; ++index) {
        cin >> values[index];
        tree.add(index, values[index]);
    }
    for (int query = 0; query < query_count; ++query) {
        int type;
        cin >> type;
        if (type == 1) {
            int position;
            long long value;
            cin >> position >> value;
            tree.add(position, value - values[position]);
            values[position] = value;
        } else {
            int left, right;
            cin >> left >> right;
            cout << tree.range_sum(left, right) << '\n';
        }
    }
}

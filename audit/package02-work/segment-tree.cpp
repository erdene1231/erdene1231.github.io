#include <bits/stdc++.h>
using namespace std;

class SegmentTree {
    int count;
    vector<long long> tree;
    void build(int node, int left, int right, const vector<long long>& values) {
        if (left == right) {
            tree[node] = values[left];
            return;
        }
        int middle = left + (right - left) / 2;
        build(node * 2, left, middle, values);
        build(node * 2 + 1, middle + 1, right, values);
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }
    void assign(int node, int left, int right, int position, long long value) {
        if (left == right) {
            tree[node] = value;
            return;
        }
        int middle = left + (right - left) / 2;
        if (position <= middle) {
            assign(node * 2, left, middle, position, value);
        } else {
            assign(node * 2 + 1, middle + 1, right, position, value);
        }
        tree[node] = tree[node * 2] + tree[node * 2 + 1];
    }
    long long query_sum(int node, int left, int right, int query_left, int query_right) const {
        if (query_right < left || right < query_left) {
            return 0;
        }
        if (query_left <= left && right <= query_right) {
            return tree[node];
        }
        int middle = left + (right - left) / 2;
        return query_sum(node * 2, left, middle, query_left, query_right)
             + query_sum(node * 2 + 1, middle + 1, right, query_left, query_right);
    }
public:
    explicit SegmentTree(const vector<long long>& values)
        : count(static_cast<int>(values.size()) - 1), tree(4 * count) {
        build(1, 1, count, values);
    }
    void assign(int position, long long value) {
        assign(1, 1, count, position, value);
    }
    long long range_sum(int left, int right) const {
        return query_sum(1, 1, count, left, right);
    }
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count, query_count;
    cin >> count >> query_count;
    vector<long long> values(count + 1);
    for (int index = 1; index <= count; ++index) {
        cin >> values[index];
    }
    SegmentTree tree(values);
    for (int query = 0; query < query_count; ++query) {
        int type;
        cin >> type;
        if (type == 1) {
            int position;
            long long value;
            cin >> position >> value;
            tree.assign(position, value);
        } else {
            int left, right;
            cin >> left >> right;
            cout << tree.range_sum(left, right) << '\n';
        }
    }
}

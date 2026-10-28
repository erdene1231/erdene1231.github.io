#include <bits/stdc++.h>
using namespace std;

class LazySum {
    int count;
    vector<long long> sum, pending_set, pending_add;
    vector<bool> has_set;
    void build(int node, int left, int right, const vector<long long>& values) {
        if (left == right) {
            sum[node] = values[left];
            return;
        }
        int middle = left + (right - left) / 2;
        build(node * 2, left, middle, values);
        build(node * 2 + 1, middle + 1, right, values);
        sum[node] = sum[node * 2] + sum[node * 2 + 1];
    }
    void apply_set(int node, int length, long long value) {
        sum[node] = value * length;
        has_set[node] = true;
        pending_set[node] = value;
        pending_add[node] = 0;
    }
    void apply_add(int node, int length, long long value) {
        sum[node] += value * length;
        pending_add[node] += value;
    }
    void push(int node, int left, int right) {
        if (left == right) {
            return;
        }
        int middle = left + (right - left) / 2;
        if (has_set[node]) {
            apply_set(node * 2, middle - left + 1, pending_set[node]);
            apply_set(node * 2 + 1, right - middle, pending_set[node]);
            has_set[node] = false;
        }
        if (pending_add[node] != 0) {
            apply_add(node * 2, middle - left + 1, pending_add[node]);
            apply_add(node * 2 + 1, right - middle, pending_add[node]);
            pending_add[node] = 0;
        }
    }
    void update(int node, int left, int right, int query_left, int query_right,
                long long value, bool assignment) {
        if (query_right < left || right < query_left) {
            return;
        }
        if (query_left <= left && right <= query_right) {
            if (assignment) {
                apply_set(node, right - left + 1, value);
            } else {
                apply_add(node, right - left + 1, value);
            }
            return;
        }
        push(node, left, right);
        int middle = left + (right - left) / 2;
        update(node * 2, left, middle, query_left, query_right, value, assignment);
        update(node * 2 + 1, middle + 1, right, query_left, query_right, value, assignment);
        sum[node] = sum[node * 2] + sum[node * 2 + 1];
    }
    long long query(int node, int left, int right, int query_left, int query_right) {
        if (query_right < left || right < query_left) {
            return 0;
        }
        if (query_left <= left && right <= query_right) {
            return sum[node];
        }
        push(node, left, right);
        int middle = left + (right - left) / 2;
        return query(node * 2, left, middle, query_left, query_right)
             + query(node * 2 + 1, middle + 1, right, query_left, query_right);
    }
public:
    explicit LazySum(const vector<long long>& values)
        : count(static_cast<int>(values.size()) - 1), sum(4 * count),
          pending_set(4 * count), pending_add(4 * count), has_set(4 * count) {
        build(1, 1, count, values);
    }
    void add(int left, int right, long long value) {
        update(1, 1, count, left, right, value, false);
    }
    void assign(int left, int right, long long value) {
        update(1, 1, count, left, right, value, true);
    }
    long long range_sum(int left, int right) {
        return query(1, 1, count, left, right);
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
    LazySum tree(values);
    for (int query = 0; query < query_count; ++query) {
        int type, left, right;
        cin >> type >> left >> right;
        if (type == 3) {
            cout << tree.range_sum(left, right) << '\n';
        } else {
            long long value;
            cin >> value;
            if (type == 1) {
                tree.add(left, right, value);
            } else {
                tree.assign(left, right, value);
            }
        }
    }
}

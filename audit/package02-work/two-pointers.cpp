#include <algorithm>
#include <iostream>
#include <utility>
#include <vector>
using namespace std;

struct Entry {
    long long value;
    int original_index;
};

pair<int, int> find_pair(vector<Entry> entries, long long target) {
    sort(entries.begin(), entries.end(), [](const Entry& first, const Entry& second) {
        return first.value < second.value;
    });
    int left = 0;
    int right = static_cast<int>(entries.size()) - 1;
    while (left < right) {
        long long sum = entries[left].value + entries[right].value;
        if (sum == target) {
            return {entries[left].original_index, entries[right].original_index};
        }
        if (sum < target) {
            ++left;
        } else {
            --right;
        }
    }
    return {-1, -1};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int size;
    long long target;
    cin >> size >> target;
    vector<Entry> entries(size);
    for (int index = 0; index < size; ++index) {
        cin >> entries[index].value;
        entries[index].original_index = index + 1;
    }
    pair<int, int> answer = find_pair(entries, target);
    if (answer.first == -1) {
        cout << "IMPOSSIBLE\n";
    } else {
        cout << answer.first << ' ' << answer.second << '\n';
    }
    return 0;
}

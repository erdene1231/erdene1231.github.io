#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;
using Integer = unsigned long long;

bool can_produce(const vector<Integer>& times, Integer target, Integer duration) {
    Integer produced = 0;
    for (Integer time : times) {
        Integer units = duration / time;
        if (units >= target - produced) {
            return true;
        }
        produced += units;
    }
    return false;
}

Integer minimum_time(const vector<Integer>& times, Integer target) {
    Integer fastest = *min_element(times.begin(), times.end());
    Integer left = 0;
    Integer right = fastest * target;
    while (left < right) {
        Integer middle = left + (right - left) / 2;
        if (can_produce(times, target, middle)) {
            right = middle;
        } else {
            left = middle + 1;
        }
    }
    return left;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int machine_count;
    Integer target;
    cin >> machine_count >> target;
    vector<Integer> times(machine_count);
    for (Integer& time : times) {
        cin >> time;
    }
    cout << minimum_time(times, target) << '\n';
    return 0;
}

#include <iostream>
#include <queue>
#include <stack>
#include <string>
using namespace std;

void remove_stack(stack<long long>& pending) {
    if (pending.empty()) {
        cout << "EMPTY\n";
        return;
    }
    cout << pending.top() << '\n';
    pending.pop();
}

void remove_queue(queue<long long>& waiting) {
    if (waiting.empty()) {
        cout << "EMPTY\n";
        return;
    }
    cout << waiting.front() << '\n';
    waiting.pop();
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int command_count;
    cin >> command_count;
    stack<long long> pending;
    queue<long long> waiting;

    for (int step = 0; step < command_count; ++step) {
        string command;
        cin >> command;
        if (command == "S+" || command == "Q+") {
            long long value;
            cin >> value;
            if (command == "S+") {
                pending.push(value);
            } else {
                waiting.push(value);
            }
        } else if (command == "S-") {
            remove_stack(pending);
        } else {
            remove_queue(waiting);
        }
    }
    return 0;
}

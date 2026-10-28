#include <iostream>
#include <string>
using namespace std;
using Mask = unsigned long long;

int count_members(Mask value) {
    int count = 0;
    while (value != 0) {
        value &= value - Mask{1};
        ++count;
    }
    return count;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int width, command_count;
    cin >> width >> command_count;
    Mask universe = (Mask{1} << width) - Mask{1};
    Mask members = 0;

    for (int step = 0; step < command_count; ++step) {
        string command;
        cin >> command;
        if (command == "COUNT") {
            cout << count_members(members) << '\n';
        } else if (command == "FLIP") {
            members = (~members) & universe;
        } else {
            int position;
            cin >> position;
            Mask bit = Mask{1} << position;
            if (command == "SET") {
                members |= bit;
            } else if (command == "CLEAR") {
                members &= ~bit;
            } else if (command == "TOGGLE") {
                members ^= bit;
            } else {
                cout << ((members & bit) != 0) << '\n';
            }
        }
    }
    return 0;
}

#include <bits/stdc++.h>
using namespace std;

struct Guest {
    long long arrival, departure;
    int index;
};

pair<int, vector<int>> allocate_rooms(vector<Guest> guests) {
    sort(guests.begin(), guests.end(), [](const Guest& left, const Guest& right) {
        return tie(left.arrival, left.departure, left.index)
             < tie(right.arrival, right.departure, right.index);
    });
    using Booking = pair<long long, int>;
    priority_queue<Booking, vector<Booking>, greater<Booking>> rooms;
    vector<int> assignment(guests.size());
    int room_count = 0;
    for (const Guest& guest : guests) {
        int room;
        if (!rooms.empty() && rooms.top().first < guest.arrival) {
            room = rooms.top().second;
            rooms.pop();
        } else {
            room = ++room_count;
        }
        assignment[guest.index] = room;
        rooms.push({guest.departure, room});
    }
    return {room_count, assignment};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int count;
    cin >> count;
    vector<Guest> guests(count);
    for (int index = 0; index < count; ++index) {
        cin >> guests[index].arrival >> guests[index].departure;
        guests[index].index = index;
    }
    auto [room_count, assignment] = allocate_rooms(guests);
    cout << room_count << '\n';
    for (int index = 0; index < count; ++index) {
        cout << assignment[index] << (index + 1 == count ? '\n' : ' ');
    }
    if (count == 0) {
        cout << '\n';
    }
}

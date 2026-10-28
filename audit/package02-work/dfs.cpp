#include <iostream>
#include <vector>
using namespace std;
using Graph = vector<vector<int>>;

struct Frame {
    int vertex;
    size_t next_index;
};

struct Traversal {
    vector<int> parent;
    vector<int> entered;
    vector<int> finished;
};

Traversal depth_first_forest(const Graph& graph) {
    int vertex_count = static_cast<int>(graph.size()) - 1;
    Traversal result{vector<int>(vertex_count + 1, 0),
                     vector<int>(vertex_count + 1, 0),
                     vector<int>(vertex_count + 1, 0)};
    vector<Frame> frames;
    int timer = 0;

    for (int start = 1; start <= vertex_count; ++start) {
        if (result.entered[start] != 0) {
            continue;
        }
        result.entered[start] = ++timer;
        frames.push_back({start, 0});
        while (!frames.empty()) {
            int vertex = frames.back().vertex;
            if (frames.back().next_index == graph[vertex].size()) {
                result.finished[vertex] = ++timer;
                frames.pop_back();
                continue;
            }
            int next = graph[vertex][frames.back().next_index];
            ++frames.back().next_index;
            if (result.entered[next] != 0) {
                continue;
            }
            result.parent[next] = vertex;
            result.entered[next] = ++timer;
            frames.push_back({next, 0});
        }
    }
    return result;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int vertex_count, edge_count;
    cin >> vertex_count >> edge_count;
    Graph graph(vertex_count + 1);
    for (int edge = 0; edge < edge_count; ++edge) {
        int first, second;
        cin >> first >> second;
        graph[first].push_back(second);
        graph[second].push_back(first);
    }

    Traversal result = depth_first_forest(graph);
    for (int vertex = 1; vertex <= vertex_count; ++vertex) {
        cout << vertex << ' ' << result.parent[vertex] << ' '
             << result.entered[vertex] << ' ' << result.finished[vertex] << '\n';
    }
    return 0;
}

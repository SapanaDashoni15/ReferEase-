#include <iostream>
#include <vector>
#include <map>
#include <deque>

std::vector<int> GetAllowedRequests(std::vector<int> user, std::vector<int> timestamp, int k) {
    std::map<int, std::deque<int>> user_allowed_timestamps;
    
    int n = user.size();
    std::vector<int> result(n);
    
    const int window_size = 60;

    for (int i = 0; i < n; ++i) {
        int current_user_id = user[i];
        int current_timestamp = timestamp[i];
        
        std::deque<int>& allowed_times = user_allowed_timestamps[current_user_id];
        
        while (!allowed_times.empty() && allowed_times.front() <= current_timestamp - window_size) {
            allowed_times.pop_front();
        }
        
        if (allowed_times.size() < k) {
            result[i] = 1;
            allowed_times.push_back(current_timestamp);
        } else {
            result[i] = 0;
        }
    }
    
    return result;
}

void print_vector(const std::vector<int>& vec) {
    for (int i = 0; i < vec.size(); ++i) {
        std::cout << vec[i] << (i == vec.size() - 1 ? "" : " ");
    }
    std::cout << "\n";
}

int main() {
    std::cout << "--- API Rate Limiter Test Cases ---\n";

    // Test Case 1: Example from problem (k=2)
    // Input: user=[1, 1, 1], timestamp=[6, 10, 65], k=2
    // Expected Output: 1 1 0
    std::vector<int> user1 = {1, 1, 1};
    std::vector<int> timestamp1 = {6, 10, 65};
    int k1 = 2;
    std::vector<int> result1 = GetAllowedRequests(user1, timestamp1, k1);
    std::cout << "\nTest Case 1 (k=2):\n";
    std::cout << "Expected: 1 1 0\n";
    std::cout << "Actual:   ";
    print_vector(result1);

    // Test Case 2: Sample Case 0 (k=1, unique users)
    // Input: user=[1, 2, 3], timestamp=[1, 10, 70], k=1
    // Expected Output: 1 1 1
    std::vector<int> user2 = {1, 2, 3};
    std::vector<int> timestamp2 = {1, 10, 70};
    int k2 = 1;
    std::vector<int> result2 = GetAllowedRequests(user2, timestamp2, k2);
    std::cout << "\nTest Case 2 (k=1, unique users):\n";
    std::cout << "Expected: 1 1 1\n";
    std::cout << "Actual:   ";
    print_vector(result2);

    // Test Case 3: Sample Case 1 (k=1, same user)
    // Input: user=[1, 1, 1], timestamp=[1, 10, 20], k=1
    // Expected Output: 1 0 0
    std::vector<int> user3 = {1, 1, 1};
    std::vector<int> timestamp3 = {1, 10, 20};
    int k3 = 1;
    std::vector<int> result3 = GetAllowedRequests(user3, timestamp3, k3);
    std::cout << "\nTest Case 3 (k=1, same user):\n";
    std::cout << "Expected: 1 0 0\n";
    std::cout << "Actual:   ";
    print_vector(result3);
    
    return 0;
}
def max_sum_subarray(arr, k):
    n = len(arr)
    if n < k:
        return None  # window size too big

    # Step 1: Compute the sum of the first window
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Step 2: Slide the window
    for i in range(k, n):
        # remove the element going out and add the new one
        window_sum = window_sum - arr[i - k] + arr[i]
        max_sum = max(max_sum, window_sum)

    return max_sum
print(max_sum_subarray)


# Example usage:
arr = [2, 1, 5, 1, 3, 2]
k = 3
print(max_sum_subarray(arr, k))  # Output: 9 (subarray [5,1,3])

paragraph = "This is the first sentence. Here is the second one! And this is the third?"

# Split by sentence delimiters
import re
sentences = re.split(r'(?<=[.!?]) +', paragraph)

print(sentences)
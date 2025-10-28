import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import hadamard


def lfsr_sequence(poly, seed, n):
    """Generate an m-sequence using given feedback polynomial (as taps)."""
    state = seed.copy()
    seq = np.zeros(2**n - 1, dtype=int)
    for i in range(len(seq)):
        seq[i] = state[-1]
        feedback = np.mod(np.sum(state[np.array(poly) - 1]), 2)
        state[1:] = state[:-1]
        state[0] = feedback
    return seq

def gold_codes(n, poly1, poly2, seed):
    """Generate Gold code family for degree n LFSRs with given feedback taps."""
    s1 = lfsr_sequence(poly1, seed.copy(), n)
    s2 = lfsr_sequence(poly2, seed.copy(), n)
    N = len(s1)
    codes = []

    for shift in range(N):
        s2_shift = np.roll(s2, shift)
        codes.append(np.bitwise_xor(s1, s2_shift))
    # Add original sequences too
    codes.append(s1)
    codes.append(s2)
    return np.array(codes)




if __name__ == "__main__":

    # Example: n = 5 (length = 31)
    # Preferred polynomials for n=5 are often [5,2] and [5,4,3,2]
    n = 5
    poly1 = [5, 2]          # x^5 + x^2 + 1
    poly2 = [5, 4, 3, 2]    # x^5 + x^4 + x^3 + x^2 + 1
    seed = np.array([1, 0, 0, 0, 1])

    codes = gold_codes(n, poly1, poly2, seed)


    print("Generated", len(codes), "Gold codes of length", len(codes[0]))
    print("First Gold code:\n", codes[0])

    h_test = hadamard(32)
    h_test = h_test[1, :]
    a = codes[0]
    b = codes[1]
    corr = np.correlate(-(2*np.tile(a, 10) - 1), 2*a - 1, mode='full')  # map 0→-1, 1→+1
    corr2 = np.correlate(np.tile(h_test, 10), h_test, mode='full')

    plt.plot(corr)
    plt.plot(corr2)
    plt.title("Cross-correlation between two Gold codes")
    plt.show()

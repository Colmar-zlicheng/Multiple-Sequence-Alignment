

def compute_cost(q1, q2):
    assert len(q1) == len(q2), "the input two queries should have same length"
    cost = 0
    for i in range(len(q1)):
        if q1[i] == q2[i]:
            cost += 0
        elif q1[i] != q2[i] and q1[i] != "-" and q2[i] != "-":
            cost += 4
        else:
            cost += 3
    return cost


def get_query_from_path_pairwise(path, q1, q2):
    q_1 = []
    q_2 = []
    i = len(q1) - 1
    j = len(q2) - 1
    gap = "-"
    for p in path:
        if p == 0:
            q_1.append(q1[i])
            q_2.append(q2[j])
            i = i - 1
            j = j - 1
        elif p == 1:
            q_1.append(q1[i])
            q_2.append(gap)
            i = i - 1
        elif p == 2:
            q_1.append(gap)
            q_2.append(q2[j])
            j = j - 1
        else:
            assert False, "p should be in [0, 1, 2]"
    q_1 = q_1[::-1]
    q_2 = q_2[::-1]
    q_1_str = "".join(q_1)
    q_2_str = "".join(q_2)
    return q_1_str, q_2_str


def get_query_from_path_three(path, q1, q2, q0):
    q_1 = []
    q_2 = []
    q_0 = []
    i = len(q1) - 1
    j = len(q2) - 1
    k = len(q0) - 1
    gap = "-"
    for p in path:
        if p == 0:
            q_1.append(q1[i])
            q_2.append(q2[j])
            q_0.append(q0[k])
            i = i - 1
            j = j - 1
            k = k - 1
        elif p == 1:
            q_1.append(q1[i])
            q_2.append(gap)
            q_0.append(gap)
            i = i - 1
        elif p == 2:
            q_1.append(gap)
            q_2.append(q2[j])
            q_0.append(gap)
            j = j - 1
        elif p == 3:
            q_1.append(gap)
            q_2.append(gap)
            q_0.append(q0[k])
            k = k - 1
        elif p == 4:
            q_1.append(q1[i])
            q_2.append(q2[j])
            q_0.append(gap)
            i = i - 1
            j = j - 1
        elif p == 5:
            q_1.append(gap)
            q_2.append(q2[j])
            q_0.append(q0[k])
            k = k - 1
            j = j - 1
        elif p == 6:
            q_1.append(q1[i])
            q_2.append(gap)
            q_0.append(q0[k])
            i = i - 1
            k = k - 1
        else:
            assert False, "p should be in [0, 1, 2, 3, 4, 5, 6]"
    q_1 = q_1[::-1]
    q_2 = q_2[::-1]
    q_0 = q_0[::-1]
    q_1_str = "".join(q_1)
    q_2_str = "".join(q_2)
    q_0_str = "".join(q_0)
    return q_1_str, q_2_str, q_0_str

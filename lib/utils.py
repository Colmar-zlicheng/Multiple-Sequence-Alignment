import numpy as np


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


def get_map_pairwise(q1, q2):
    m = len(q1)
    n = len(q2)
    gap = 3
    error = 4
    map = np.zeros((m + 1, n + 1), dtype=np.int)
    for i in range(m+1):
        for j in range(n+1):
            # map(0,0) = 0
            if i == 0 and j == 0:
                map[i][j] = 0
            elif i - 1 < 0:  # first row
                map[i][j] = map[i][j - 1] + gap
            elif j - 1 < 0:  # first column
                map[i][j] = map[i - 1][j] + gap
            else:
                if q1[i-1] == q2[j-1]:
                    score = 0
                else:
                    score = error
                map[i][j] = min(map[i - 1][j - 1] + score, map[i - 1][j] + gap, map[i][j - 1] + gap)
    return map


def get_score(q1, q2, q0, i, j, k):
    error = 4
    if q1[i - 1] == q2[j - 1]:
        score_ij = 0
    else:
        score_ij = error

    if q0[k - 1] == q2[j - 1]:
        score_jk = 0
    else:
        score_jk = error

    if q1[i - 1] == q0[k - 1]:
        score_ik = 0
    else:
        score_ik = error

    return score_ij, score_jk, score_ik


def get_map_three(q1, q2, q0):
    m = len(q1)
    n = len(q2)
    l = len(q0)
    gap = 3
    error = 4
    map = np.zeros((m + 1, n + 1, l + 1), dtype=np.int)
    for i in range(m + 1):
        for j in range(n + 1):
            for k in range(l + 1):
                # map(0,0) = 0
                if i == 0 and j == 0 and k == 0:
                    map[i][j][k] = 0
                elif i - 1 < 0 and k - 1 < 0:  # j
                    if q1[i - 1] == q0[k - 1]:
                        score = 0
                    else:
                        score = error
                    map[i][j][k] = map[i][j - 1][k] + gap + gap + score
                elif j - 1 < 0 and k - 1 < 0:  # i
                    if q0[k - 1] == q2[j - 1]:
                        score = 0
                    else:
                        score = error
                    map[i][j][k] = map[i - 1][j][k] + gap + gap + score
                elif i - 1 < 0 and j - 1 < 0:  # k
                    if q1[i - 1] == q2[j - 1]:
                        score = 0
                    else:
                        score = error
                    map[i][j][k] = map[i][j][k-1] + gap + gap + score
                elif k - 1 < 0:  # ij
                    score_ij, score_jk, score_ik = get_score(q1, q2, q0, i, j, k)
                    map[i][j][k] = min(map[i - 1][j - 1][k] + score_ij + gap + gap,\
                                       map[i - 1][j][k] + gap + gap + score_jk,\
                                       map[i][j - 1][k] + gap + gap + score_ik)
                elif i - 1 < 0:  # jk
                    score_ij, score_jk, score_ik = get_score(q1, q2, q0, i, j, k)
                    map[i][j][k] = min(map[i][j - 1][k - 1] + score_jk + gap + gap,\
                                       map[i][j][k - 1] + gap + gap + score_ij,
                                       map[i][j - 1][k] + gap + gap + score_ik)
                elif j - 1 < 0:  # ik
                    score_ij, score_jk, score_ik = get_score(q1, q2, q0, i, j, k)
                    map[i][j][k] = min(map[i - 1][j][k - 1] + score_ik + gap +gap,\
                                       map[i - 1][j][k] + gap + gap + score_jk,\
                                       map[i][j][k - 1] + gap + gap + score_ij)
                else:
                    score_ij, score_jk, score_ik = get_score(q1, q2, q0, i, j, k)
                    map[i][j][k] = min(map[i - 1][j - 1][k - 1] + score_ij + score_jk + score_ik,\
                                       map[i][j - 1][k - 1] + score_jk + gap + gap,\
                                       map[i - 1][j][k - 1] + score_ik + gap +gap,\
                                       map[i - 1][j - 1][k] + score_ij + gap + gap,\
                                       map[i - 1][j][k] + gap + gap + score_jk,\
                                       map[i][j - 1][k] + gap + gap + score_ik,\
                                       map[i][j][k - 1] + gap + gap + score_ij)
    return map


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

import numpy as np
from tqdm import tqdm
from lib.utils import compute_cost, get_query_from_path_pairwise, get_query_from_path_three



class DP:

    def get_path_pairwise(self, map, m, n):
        path = []
        i = m
        j = n
        while i != 0 or j != 0:
            if i == 0 and j > 0:
                path.append(2)
                j = j - 1
            elif i > 0 and j == 0:
                path.append(1)
                i = i - 1
            elif i > 0 and j > 0:
                last_min = min(map[i - 1][j - 1], map[i - 1][j], map[i][j - 1])
                if last_min == map[i - 1][j - 1]:
                    path.append(0)
                    i = i - 1
                    j = j - 1
                elif last_min == map[i - 1][j]:
                    path.append(1)
                    i = i - 1
                else:
                    path.append(2)
                    j = j - 1
            else:
                assert False, "i and j couldn't less than 0"

        return path

    def get_path_three(self, map, m, n, l):
        path = []
        i = m
        j = n
        k = l
        while i != 0 or j != 0 or k != 0:
            if i == 0 and j > 0 and k > 0:
                last_min = min(map[i][j - 1][k - 1], map[i][j][k - 1], map[i][j - 1][k])
                if last_min == map[i][j - 1][k - 1]:
                    path.append(5)
                    k = k - 1
                    j = j - 1
                elif last_min == map[i][j][k - 1]:
                    path.append(3)
                    k = k - 1
                else:
                    path.append(2)
                    j = j - 1
            elif i > 0 and j == 0 and k > 0:
                last_min = min(map[i - 1][j][k - 1], map[i - 1][j][k], map[i][j][k - 1])
                if last_min == map[i - 1][j][k - 1]:
                    path.append(6)
                    i = i - 1
                    k = k - 1
                elif last_min == map[i - 1][j][k]:
                    path.append(1)
                    i = i - 1
                else:
                    path.append(3)
                    k = k - 1
            elif i > 0 and j > 0 and k == 0:
                last_min = min(map[i - 1][j - 1][k], map[i - 1][j][k], map[i][j - 1][k])
                if last_min == map[i - 1][j - 1][k]:
                    path.append(4)
                    i = i - 1
                    j = j - 1
                elif last_min == map[i - 1][j][k]:
                    path.append(1)
                    i = i - 1
                else:
                    path.append(2)
                    j = j - 1
            elif i == 0 and j == 0 and k > 0:
                path.append(3)
                k = k - 1
            elif i == 0 and j > 0 and k == 0:
                path.append(2)
                j = j - 1
            elif i > 0 and j == 0 and k == 0:
                path.append(1)
                i = i - 1
            elif i > 0 and j > 0 and k > 0:
                last_min = min(map[i - 1][j - 1][k - 1],\
                               map[i][j - 1][k - 1],\
                               map[i - 1][j][k - 1],\
                               map[i - 1][j - 1][k],\
                               map[i - 1][j][k],\
                               map[i][j - 1][k],\
                               map[i][j][k - 1])
                if last_min == map[i - 1][j - 1][k - 1]:
                    path.append(0)
                    i = i - 1
                    j = j - 1
                    k = k - 1
                elif last_min == map[i][j - 1][k - 1]:
                    path.append(5)
                    k = k - 1
                    j = j - 1
                elif last_min == map[i - 1][j][k - 1]:
                    path.append(6)
                    i = i - 1
                    k = k - 1
                elif last_min == map[i - 1][j - 1][k]:
                    path.append(4)
                    i = i - 1
                    j = j - 1
                elif last_min == map[i - 1][j][k]:
                    path.append(1)
                    i = i - 1
                elif last_min == map[i][j - 1][k]:
                    path.append(2)
                    j = j - 1
                elif last_min == map[i][j][k - 1]:
                    path.append(3)
                    k = k - 1
            else:
                assert False, "i and j and k couldn't less than 0"

        return path

    def get_map_pairwise(self, q1, q2):
        m = len(q1)
        n = len(q2)
        gap = 3
        error = 4
        map = np.zeros((m + 1, n + 1), dtype=np.int)
        for i in range(m + 1):
            for j in range(n + 1):
                # map(0,0) = 0
                if i == 0 and j == 0:
                    map[i][j] = 0
                elif i - 1 < 0:  # first row
                    map[i][j] = map[i][j - 1] + gap
                elif j - 1 < 0:  # first column
                    map[i][j] = map[i - 1][j] + gap
                else:
                    if q1[i - 1] == q2[j - 1]:
                        score = 0
                    else:
                        score = error
                    map[i][j] = min(map[i - 1][j - 1] + score, map[i - 1][j] + gap, map[i][j - 1] + gap)
        return map

    def get_score(self, q1, q2, q0, i, j, k):
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

    def get_map_three(self, q1, q2, q0):
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
                        map[i][j][k] = map[i][j][k - 1] + gap + gap + score
                    elif k - 1 < 0:  # ij
                        score_ij, score_jk, score_ik = self.get_score(q1, q2, q0, i, j, k)
                        map[i][j][k] = min(map[i - 1][j - 1][k] + score_ij + gap + gap, \
                                           map[i - 1][j][k] + gap + gap + score_jk, \
                                           map[i][j - 1][k] + gap + gap + score_ik)
                    elif i - 1 < 0:  # jk
                        score_ij, score_jk, score_ik = self.get_score(q1, q2, q0, i, j, k)
                        map[i][j][k] = min(map[i][j - 1][k - 1] + score_jk + gap + gap, \
                                           map[i][j][k - 1] + gap + gap + score_ij,
                                           map[i][j - 1][k] + gap + gap + score_ik)
                    elif j - 1 < 0:  # ik
                        score_ij, score_jk, score_ik = self.get_score(q1, q2, q0, i, j, k)
                        map[i][j][k] = min(map[i - 1][j][k - 1] + score_ik + gap + gap, \
                                           map[i - 1][j][k] + gap + gap + score_jk, \
                                           map[i][j][k - 1] + gap + gap + score_ij)
                    else:
                        score_ij, score_jk, score_ik = self.get_score(q1, q2, q0, i, j, k)
                        map[i][j][k] = min(map[i - 1][j - 1][k - 1] + score_ij + score_jk + score_ik, \
                                           map[i][j - 1][k - 1] + score_jk + gap + gap, \
                                           map[i - 1][j][k - 1] + score_ik + gap + gap, \
                                           map[i - 1][j - 1][k] + score_ij + gap + gap, \
                                           map[i - 1][j][k] + gap + gap + score_jk, \
                                           map[i][j - 1][k] + gap + gap + score_ik, \
                                           map[i][j][k - 1] + gap + gap + score_ij)
        return map

    def Align_pairwise(self, q1, q2):
        m = len(q1)
        n = len(q2)
        search_map = self.get_map_pairwise(q1, q2)
        path = self.get_path_pairwise(search_map, m, n)
        q_1, q_2 = get_query_from_path_pairwise(path, q1, q2)
        return q_1, q_2

    def Align_three(self, q1, q2, q0):
        m = len(q1)
        n = len(q2)
        l = len(q0)
        search_map = self.get_map_three(q1, q2, q0)
        path = self.get_path_three(search_map, m, n, l)
        q_1, q_2, q_0 = get_query_from_path_three(path, q1, q2, q0)
        return q_1, q_2, q_0

    def pairwise(self, database, query):
        q1_list = []
        q2_list = []
        cost_list = []
        for i in tqdm(range(len(database))):
            q_1, q_2 = self.Align_pairwise(database[i], query)
            q1_list.append(q_1)
            q2_list.append(q_2)
            cost = compute_cost(q_1, q_2)
            cost_list.append(cost)

        cost_min = min(cost_list)
        min_index = cost_list.index(cost_min)
        return q1_list[min_index], q2_list[min_index], cost_min

    def three(self, database, query):
        q1_list = []
        q2_list = []
        cost_list = []
        for i in tqdm(range(len(database))):
            for j in range(i+1, len(database)):
                tempo_list = []
                q_1_0, q_1_1, q_2 = self.Align_three(database[i], database[j], query)
                cost0 = compute_cost(q_1_0, q_2)
                cost1 = compute_cost(q_1_1, q_2)
                cost2 = compute_cost(q_1_0, q_1_1)
                cost = cost0 + cost1 + cost2
                tempo_list.append(q_1_0)
                tempo_list.append(q_1_1)
                q1_list.append(tempo_list)
                q2_list.append(q_2)
                cost_list.append(cost)

        cost_min = min(cost_list)
        min_index = cost_list.index(cost_min)
        return q1_list[min_index], q2_list[min_index], cost_min


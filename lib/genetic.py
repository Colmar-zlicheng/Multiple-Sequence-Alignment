import numpy as np
from tqdm import tqdm
from lib.utils import compute_cost, get_query_from_path_pairwise, get_query_from_path_three



class genetic:


    def Align_pairwise(self, q1, q2):

        q_1, q_2 = get_query_from_path_pairwise(path, q1, q2)
        return q_1, q_2

    def Align_three(self, q1, q2, q0):

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


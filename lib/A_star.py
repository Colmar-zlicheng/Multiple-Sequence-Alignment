from tqdm import tqdm
from lib.utils import compute_cost, get_query_from_path_pairwise, get_query_from_path_three


class order_seq_pairwise():  # ascending
    def __init__(self):
        self.data = []
        self.last_dict = {}  # create mapping from this pos to last pos  eg:  (1,2) -> (3,4) means the last position of (1,2) is (3,4)

    def append(self, tuple, last_pos=(-1, -1)):  # tuple like ( 1,1,(1,2)) refering to (F,G,(this_position))
        insert_tag = True
        if self.data == []:
            self.data.append(tuple)
            self.last_dict[tuple[2]] = last_pos
        else:
            for item in self.data:
                if tuple[2] == item[2]:
                    if tuple[1] < item[1]:
                        self.data.remove(item)
                    else:
                        insert_tag = False
                    break
            if insert_tag:
                is_insert = False
                for id, item in enumerate(self.data):
                    if tuple[0] <= item[0]:
                        self.data.insert(id, tuple)
                        self.last_dict[tuple[2]] = last_pos
                        is_insert = True
                        break
                if not is_insert:
                    self.data.append(tuple)
                    self.last_dict[tuple[2]] = last_pos

    def pop(self):
        return self.data.pop(0)

    def is_empty(self):
        if self.data == []:
            return True
        else:
            return False

class order_seq_three():  # ascending
    def __init__(self):
        self.data = []
        self.last_dict = {}  # create mapping from this pos to last pos  eg:  (1,2) -> (3,4) means the last position of (1,2) is (3,4)

    def append(self, tuple, last_pos=(-1, -1, -1)):  # tuple like ( 1,1,(1,2)) refering to (F,G,(this_position))
        insert_tag = True
        if self.data == []:
            self.data.append(tuple)
            self.last_dict[tuple[2]] = last_pos
        else:
            for item in self.data:
                if tuple[2] == item[2]:
                    if tuple[1] < item[1]:
                        self.data.remove(item)
                    else:
                        insert_tag = False
                    break
            if insert_tag:
                is_insert = False
                for id, item in enumerate(self.data):
                    if tuple[0] <= item[0]:
                        self.data.insert(id, tuple)
                        self.last_dict[tuple[2]] = last_pos
                        is_insert = True
                        break
                if not is_insert:
                    self.data.append(tuple)
                    self.last_dict[tuple[2]] = last_pos

    def pop(self):
        return self.data.pop(0)

    def is_empty(self):
        if self.data == []:
            return True
        else:
            return False


def A_star_pairwise(pos_start, pos_end, q1, q2, m, n):

    open_list = order_seq_pairwise()
    close_list = []
    open_list.append((0, 0, pos_start))

    while True:
        if open_list.is_empty():
            return False, {}
        else:
            temp_tuple = open_list.pop()
        pos = temp_tuple[2]
        if pos == pos_end:
            return True, open_list.last_dict
        F = temp_tuple[0]
        G = temp_tuple[1]
        x = temp_tuple[2][0]
        y = temp_tuple[2][1]

        gap = 3
        error = 4

        if y + 1 < n and (x, y + 1) not in close_list:  # right
            New_G = G + gap
            New_H = abs(pos_end[0] - x) + abs(pos_end[1] - (y + 1))
            New_H = New_H // 2
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x, y + 1))
            open_list.append(New_tuple, pos)
        if x + 1 < m and (x + 1, y) not in close_list:  # down
            New_G = G + gap
            New_H = abs(pos_end[0] - (x + 1)) + abs(pos_end[1] - y)
            New_H = New_H // 2
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x + 1, y))
            open_list.append(New_tuple, pos)
        if x + 1 < m and y + 1 < n and (x + 1, y + 1) not in close_list:
            if q1[x] == q2[y]:
                score = 1
            else:
                score = error
            New_G = G + score
            New_H = abs(pos_end[0] - (x + 1)) + abs(pos_end[1] - (y + 1))
            New_H = New_H // 2
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x + 1, y + 1))
            open_list.append(New_tuple, pos)

        close_list.append(pos)


def A_star_three(pos_start, pos_end, q1, q2, q0, m, n, l):

    open_list = order_seq_three()
    close_list = []
    open_list.append((0, 0, pos_start))

    while True:
        if open_list.is_empty():
            return False, {}
        else:
            temp_tuple = open_list.pop()
        pos = temp_tuple[2]
        if pos == pos_end:
            return True, open_list.last_dict
        F = temp_tuple[0]
        G = temp_tuple[1]
        x = temp_tuple[2][0]
        y = temp_tuple[2][1]
        z = temp_tuple[2][2]

        gap = 3
        error = 4
        s = 4

        if x + 1 < m and (x + 1, y, z) not in close_list:
            if z > l - 2 or y > n - 2:
                continue
            if q2[y] == q0[z]:
                score = 0
            else:
                score = error
            New_G = G + gap + gap + score
            New_H = abs(pos_end[0] - (x + 1)) + abs(pos_end[1] - y) + abs(pos_end[2] - z)
            New_H = New_H * s
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x + 1, y, z))
            open_list.append(New_tuple, pos)
        if y + 1 < n and (x, y + 1, z) not in close_list:
            if x > m - 2 or z > l - 2:
                continue
            if q1[x] == q0[z]:
                score = 0
            else:
                score = error
            New_G = G + gap + gap + score
            New_H = abs(pos_end[0] - x) + abs(pos_end[1] - (y + 1)) + abs(pos_end[2] - z)
            New_H = New_H * s
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x, y + 1, z))
            open_list.append(New_tuple, pos)
        if z + 1 < l and (x, y, z + 1) not in close_list:
            if x > m - 2 or y > n - 2:
                continue
            if q2[y] == q1[x]:
                score = 0
            else:
                score = error
            New_G = G + gap + gap + score
            New_H = abs(pos_end[0] - x) + abs(pos_end[1] - y) + abs(pos_end[2] - (z + 1))
            New_H = New_H * s
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x, y , z + 1))
            open_list.append(New_tuple, pos)
        if x + 1 < m and y + 1 < n and (x + 1, y + 1, z) not in close_list:
            if z > l - 2:
                continue
            if q2[y] == q1[x]:
                score = 0
            else:
                score = error
            New_G = G + gap + gap + score
            New_H = abs(pos_end[0] - (x + 1)) + abs(pos_end[1] - (y + 1)) + abs(pos_end[2] - z)
            New_H = New_H * s
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x + 1, y + 1, z))
            open_list.append(New_tuple, pos)
        if x + 1 < m and z + 1 < l and (x + 1, y, z + 1) not in close_list:
            if y > n - 2:
                continue
            if q1[x] == q0[z]:
                score = 0
            else:
                score = error
            New_G = G + gap + gap + score
            New_H = abs(pos_end[0] - (x + 1)) + abs(pos_end[1] - y) + abs(pos_end[2] - (z + 1))
            New_H = New_H * s
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x + 1, y, z + 1))
            open_list.append(New_tuple, pos)
        if z + 1 < l and y + 1 < n and (x, y + 1, z + 1) not in close_list:
            if x > m - 2:
                continue
            if q2[y] == q0[z]:
                score = 0
            else:
                score = error
            New_G = G + gap + gap + score
            New_H = abs(pos_end[0] - x) + abs(pos_end[1] - (y + 1)) + abs(pos_end[2] - (z + 1))
            New_H = New_H * s
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x, y + 1, z + 1))
            open_list.append(New_tuple, pos)
        if x + 1 < m and y + 1 < n and z + 1 < l and (x + 1, y + 1, z + 1) not in close_list:
            if q2[y] == q1[x]:
                score_xy = 0
            else:
                score_xy = error
            if q0[z] == q1[x]:
                score_xz = 0
            else:
                score_xz = error
            if q2[y] == q0[z]:
                score_yz = 0
            else:
                score_yz = error
            New_G = G + score_xy + score_xz + score_yz
            New_H = abs(pos_end[0] - (x + 1)) + abs(pos_end[1] - (y + 1)) + abs(pos_end[2] - (z + 1))
            New_H = New_H * s
            New_F = New_G + New_H
            New_tuple = (New_F, New_G, (x + 1, y + 1, z + 1))
            open_list.append(New_tuple, pos)
        close_list.append(pos)


def path_parser_pairwise(food_pos,last_dict):
    path_list = []
    path_list.append(food_pos)
    temp = last_dict[food_pos]
    while temp != (-1, -1):
        path_list.append(temp)
        temp = last_dict[temp]
    return path_list


def path_parser_three(food_pos,last_dict):
    path_list = []
    path_list.append(food_pos)
    temp = last_dict[food_pos]
    while temp != (-1, -1, -1):
        path_list.append(temp)
        temp = last_dict[temp]
    return path_list


class A_star:

    def get_path_pairwise(self, q1, q2):
        m = len(q1)
        n = len(q2)
        flag, dict= A_star_pairwise((0, 0), (m, n), q1, q2, m + 1, n + 1)
        assert flag, "open list is empty"
        path_list = path_parser_pairwise((m, n), dict)

        path = []
        for i in range(len(path_list)-1):
            if path_list[i][0] != path_list[i+1][0] and path_list[i][1] != path_list[i+1][1]:
                path.append(0)
            elif path_list[i][1] == path_list[i+1][1]:
                path.append(1)
            else:
                path.append(2)
        return path

    def get_path_three(self, q1, q2, q0):
        m = len(q1)
        n = len(q2)
        l = len(q0)
        flag, dict = A_star_three((0, 0, 0), (m, n, l), q1, q2, q0, m+1, n+1, l+1)
        assert flag, "open list is empty"
        path_list = path_parser_three((m, n, l), dict)
        path = []
        for i in range(len(path_list) - 1):
            x1 = path_list[i][0]
            x2 = path_list[i + 1][0]
            y1 = path_list[i][1]
            y2 = path_list[i + 1][1]
            z1 = path_list[i][2]
            z2 = path_list[i + 1][2]
            if x1 != x2 and y1 != y2 and z1 != z2:
                path.append(0)
            elif x1 == x2 and y1 != y2 and z1 != z2:
                path.append(5)
            elif x1 != x2 and y1 == y2 and z1 != z2:
                path.append(6)
            elif x1 != x2 and y1 != y2 and z1 == z2:
                path.append(4)
            elif x1 == x2 and y1 == y2 and z1 != z2:
                path.append(3)
            elif x1 != x2 and y1 == y2 and z1 == z2:
                path.append(1)
            elif x1 == x2 and y1 != y2 and z1 == z2:
                path.append(2)
        return path

    def Align_pairwise(self, q1, q2):
        path = self.get_path_pairwise(q1, q2)
        q_1, q_2 = get_query_from_path_pairwise(path, q1, q2)
        return q_1, q_2

    def Align_three(self, q1, q2, q0):
        path = self.get_path_three(q1, q2, q0)
        q_1, q_2, q_0 = get_query_from_path_three(path, q1, q2, q0)
        return q_1, q_2 ,q_0

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


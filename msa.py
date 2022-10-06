import os
import time
import argparse
from lib.DP import DP
from lib.A_star import A_star
from lib.genetic import genetic


def read_data(data_dir):
    root = data_dir["root"]
    database_dir = os.path.join(root, data_dir["database"])
    query_dir = os.path.join(root, data_dir["query"])
    with open(database_dir, 'r') as f:
        database = f.readlines()
    database = [line[:-1] for line in database] # delete \n
    with open(query_dir, 'r') as f:
        query = f.readlines()
    query = [line[:-1] for line in query] # delete \n
    query_dict ={}
    for k in range(len(query)):
        if query[k] == "2":
            i = k
        if query[k] == "3":
            j = k
    query_dict["pairwise"] = query[i+1:j]
    query_dict["three"] = query[j+1:]
    return database, query_dict


def MSA(data_dir, mode):
    if mode == "DP":
        search = DP()
    elif mode == "A_star":
        search = A_star()
    elif mode == "genetic":
        search = genetic()
    else:
        raise ValueError("no such mode")

    database, query_dict = read_data(data_dir)

    cost_pairwise = []
    q_1_pairwise = []
    q_2_pairwise = []
    print("Begin pairwise sequence alignment with ", mode)
    for i in range(len(query_dict["pairwise"])):
        query = query_dict["pairwise"][i]
        q_1, q_2, cost = search.pairwise(database, query)
        q_1_pairwise.append(q_1)
        q_2_pairwise.append(q_2)
        cost_pairwise.append(cost)

    save_pairwise_dir = './result/pairwise_' + mode
    print("Saving result of pairwise sequence alignment with ", mode)
    with open(save_pairwise_dir, 'w') as f:
        for j in range(len(cost_pairwise)):
            f.write(str(q_2_pairwise[j]) + '\n')
            f.write(str(q_1_pairwise[j]) + '\n')
            f.write('cost:' + str(cost_pairwise[j]) + '\n')

    cost_three = []
    q_1_three = []
    q_2_three = []
    print("Begin three sequence alignment with ", mode)
    for i in range(len(query_dict["three"])):
        query = query_dict["three"][i]
        q_1, q_2, cost = search.three(database, query)
        q_1_three.append(q_1)
        q_2_three.append(q_2)
        cost_three.append(cost)

    save_three_dir = './result/three_' + mode
    print("Saving result of three sequence alignment with ", mode)
    with open(save_three_dir, 'w') as f:
        for j in range(len(cost_three)):
            f.write(str(q_2_three[j]) + '\n')
            f.write(str(q_1_three[j][0]) + '\n')
            f.write(str(q_1_three[j][1]) + '\n')
            f.write('cost:' + str(cost_three[j]) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="DP",choices=["DP", "A_star", "genetic"])
    args = parser.parse_args()
    data_dir ={}
    data_dir["root"] = "./data"
    data_dir["database"] = "MSA_database.txt"
    data_dir["query"] = "MSA_query.txt"
    mode = args.mode

    start = time.time()
    MSA(data_dir, mode)
    end = time.time()
    print('Running time: %s Seconds' % (end - start))
    save_time_dir = './result/time_' + mode
    with open(save_time_dir, 'w') as f:
        f.write('Running time: %s Seconds' % (end - start))
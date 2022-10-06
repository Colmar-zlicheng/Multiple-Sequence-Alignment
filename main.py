import os
import argparse

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

def DP(a):
    print(a)

def A_star():
    print(2)

def genetic():
    print(3)

def MSA(data_dir, mode):
    database, query_dict = read_data(data_dir)
    if mode == "DP":
        search = DP()
    elif mode == "A_star":
        search = A_star()
    elif mode == "genetic":
        search = genetic()
    else:
        raise ValueError("no such mode")
    search(a=1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="DP",choices=["DP", "A_star", "genetic"])
    args = parser.parse_args()
    data_dir ={}
    data_dir["root"] = "./data"
    data_dir["database"] = "MSA_database.txt"
    data_dir["query"] = "MSA_query.txt"
    mode = args.mode
    MSA(data_dir, mode)
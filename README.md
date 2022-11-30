# Multiple-Sequence-Alignment

## DP, A*, genetic for MSA
Project 2 for CS3317-2@SJTU

Each algorithm support pairwise sequence alignment and three sequence alginment.

### dataset

```shell
data
├── MSA_database.txt
└── MSA_query.txt
```

### DP
#### run
```shell
python msa.py --mode DP
```

### A_star
#### run
```shell
python msa.py --mode A_star
```

### genetic
using external code in lib.external.py

the main code is available in https://github.com/H-Zaman/MSA-using-GA-CRO
#### run
```shell
python msa.py --mode genetic
```

### result
Results that have already benn run is saved in result_run.
If you run the code, the result will be saved in result.

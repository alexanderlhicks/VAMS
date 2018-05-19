import sys
from collections import OrderedDict, defaultdict
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder



def GetItemRow(file_name):
    dataset = []
    with open(file_name, 'r') as infile:
        for line in infile:
            tmp_items = line.split(' ')[:-1] ############
            dataset.append(tmp_items)

    te = TransactionEncoder()
    te_ary = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    return df


def Apriori(file_name, min_sup, min_conf):
    df = GetItemRow(file_name)
    from mlxtend.frequent_patterns import apriori
    return apriori(df, min_support=min_sup, use_colnames=True)




def main(path, fname):
    #id = sys.argv[0]
    #id = '0.5_tsz5_tct1.0k'
    file_name = path+fname #'../datasets/synthetic/varying_users/' + id +'.txt'
    min_sup = 0.1 #float(input('Minimum Support (between 0 and 1): '))
    min_conf = 0.1#float(input('Minimum Confidence (between 0 and 1): '))
    print(file_name, min_sup, min_conf)
    frequent_itemsets = Apriori(file_name, min_sup, min_conf)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    #print(frequent_itemsets)
    print(frequent_itemsets[(frequent_itemsets['length'] == 2)])
    frequent_itemsets.to_csv('../datasets/synthetic/varying_users/' + fname +'_Itemsets.txt', sep='\t', encoding='utf-8')


if __name__ == '__main__':
    main()


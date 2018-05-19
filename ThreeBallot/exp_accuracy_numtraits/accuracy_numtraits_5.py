import random
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import math
import itertools

shares = 3
#yes_vote = shares-1
#no_vote = shares-2
yes_vote = 2
no_vote = 1

#list_num_users = [10,100,1000, 10000, 100000]
#num_traits = 3
runs = 20


##############################################################################

deltas = {}
ratios = {}

def random_user(num_traits):
    user = {}
    for j in range(num_traits):
        user[j] = random.getrandbits(1)
    return user


def random_dataset(num_users):
    records = {}
    for i in range(num_users):
        records[i] = {}
        for j in range(num_traits):
            records[i][j] = random.getrandbits(1)
    return records


# Generates a new dataset where no one has all traits specified
def pseudorandom_dataset(num_users, lst_trait_indces):
    records = {}
    for i in range(num_users):
        records[i] = {}
        for j in range(num_traits):
            records[i][j] = random.getrandbits(1)

        #Fix users who have all these traits
        while is_user_positive(records[i], lst_trait_indces):
            records[i] = random_user(num_traits)

    return records



def empty_dataset(num_users):
    records = {}
    for i in range(num_users):
        records[i] = {}
        for j in range(num_traits):
            records[i][j] = 0
    return records


def dataset_with_trait(negative_num, positive_num, lst_trait_indces):
    records = {}
    for k in range(positive_num):
        i = negative_num+k
        records[i] = {}
        for j in range(num_traits):
            records[i][j] = random.getrandbits(1)

        for j in lst_trait_indces: #Set specific traits to True
            records[i][j] = 1

    return records


def split_dataset(dataset):
    split_dataset = []
    for i in range(len(dataset)):
        # tmp_user_share_block = shares * [traits*[0]]
        #tmp_user_share_block = [[0 for i in range(num_traits)] for j in range(shares)]
        tmp_user_share_block = []
        for s in range(shares):
            tmp_user_share_block.append({})

        #Spliting loop
        for j in range(len(dataset[0])):
            for s in range(shares): #Initialization with 0's
                tmp_user_share_block[s][j] = 0

            trait = dataset[i][j]
            if trait == 0:
                share_indces = random.sample(range(shares), no_vote)
                # share_indces = [0]
            elif trait == 1:
                share_indces = random.sample(range(shares), yes_vote)
                # share_indces = [0,1]
            else:
                print("Warning: Trait not defined.")

            for si in share_indces:
                tmp_user_share_block[si][j] = 1

        split_dataset += tmp_user_share_block.copy()
        #print(tmp_user_share_block)

    # print(split_users)
    random.shuffle(split_dataset)  # Shuffle
    # print(split_users)
    return split_dataset


##############################################################################


def is_user_positive(user, lst_trait_indces):
    for j in lst_trait_indces:
        if user[j] == 0:
            return False
    return True


def conditional_stat(dataset, lst_trait_indces=[]):
    count_A = 0.0
    count_B = 0.0

    all_but = lst_trait_indces[:-1]
    examined = lst_trait_indces[-1]

    for i in range(len(dataset)):
        has_all_traits = True
        for t in all_but:
            if dataset[i][t] != 1:
                has_all_traits = False

        if has_all_traits == True:
            if dataset[i][examined] == 1:
                count_A += 1
            else:
                count_B += 1

    print("A: " + str(count_A))
    print("B: " + str(count_B))
    return count_A / (count_A + count_B)



def trait_percent(dataset, lst_traits, num_shares=1.0):
    trait_ratios = []
    for t in lst_traits:
        tmp_sum = 0.0
        for i in range(len(dataset)): #For each user/ballot/split
            tmp_sum += dataset[i][t]

        #Find actual percentage
        if num_shares != 1:
            trait_ratios.append((tmp_sum - len(dataset)/num_shares)/(len(dataset)/num_shares)) #Remove the extra counts
            #trait_ratios.append(tmp_sum * num_shares / len(dataset) - 1.0)
        else:
            trait_ratios.append(tmp_sum/len(dataset))

    return trait_ratios


def correlation_stat(dataset, lst_traits):
    vectorA=[]
    vectorB=[]
    from scipy import stats
    import numpy

    for i in range(len(dataset)): #For each user/ballot/split
        vectorA.append(dataset[i][0])
        vectorB.append(dataset[i][1])

    corr = stats.pearsonr(vectorA,vectorB)
    #corr = stats.matthews_corrcoef(vectorA,vectorB)
    #corr = numpy.corrcoef(vectorA, vectorB)
    #print(stats.ttest_ind(vectorA, vectorB))

    print(numpy.cov(vectorA, vectorB))


    print(corr)
    print(corr[0]*corr[0])
    return corr


def association_rules(observation_vecs, candidate_vec, num_shares=1, num_X_and_Y=-1, num_X_and_not_Y=-1):
    ##Support for X
    if num_shares == 1:
        supportX = 0
        for i in range(len(observation_vecs[0])):
            all_match = True
            for vec in observation_vecs:
                if vec[i]!=1:
                    all_match=False
            if all_match:
                supportX += 1
        supportX /= len(observation_vecs[0])
    else:
        supportX = (num_X_and_not_Y + num_X_and_Y)/ (len(observation_vecs[0])/num_shares)



    ##Support for Y
    if num_shares == 1:
        supportY = np.sum(candidate_vec)/len(candidate_vec)
    else:
        supportY = (3*np.sum(candidate_vec))/len(candidate_vec)-1


    # Support for (X and Y)
    if num_shares!=1:
        supportIntersect = num_X_and_Y/(len(observation_vecs[0])/num_shares)
    else:
        supportIntersect = 0
        for i in range(len(observation_vecs[0])):
            all_match = True
            for vec in observation_vecs:
                if vec[i]!=1:
                    all_match=False

            if (all_match == True) and (candidate_vec[i] == 1):
                supportIntersect += 1
        supportIntersect /= len(candidate_vec)

    confidence = supportIntersect / supportX
    lift = (supportIntersect) / (supportX * supportY)
    conviction = 1
    #conviction = (1 - supportY) / (1 - confidence)

    return (supportX, supportY, supportIntersect, confidence, lift, conviction)


'''
def association_rules_split(observation_vecs, candidate_vec, intersection_counts):
    supports = []
    for t in observation_vecs:
        #print(t)
        supports.append((np.sum(t)-len(t)/3)/(len(t)/3))

    support_cand = np.sum(candidate_vec)/(len(candidate_vec))

    supportIntersect = intersection_counts
    supportIntersect /= (len(candidate_vec)/3)
    confidence = supportIntersect/((np.prod(supports)))
    lift       = (supportIntersect)/((np.prod(supports)*support_cand))
    conviction = (1-support_cand)/(1-confidence)

    return(supports, supportIntersect, confidence, lift, conviction)
'''


def shift(seq, n):
    n = n % len(seq)
    return seq[n:] + seq[:n]


def find_patterns(shares):
    patterns = zip(*shares)
    #print(shares)
    #print(list(patterns))
    return patterns

def compute_expected_values(shares, num_traits):
    possible_combinations = list(itertools.product([0, 1], repeat=num_traits)) #AnB, AnnotB, notAnB, notAnnotB
    counts_patterns_encountered = dict.fromkeys(possible_combinations, 0) #For two traits this would be: 00,01,10,11 etc

    permutations = []
    #permutations.append([shares[0]])
    #print(shares)
    #for r in shares[1:]:
    for r in shares:
        tmp_perms = []
        for i in range(len(r)):
            tmp_perms.append(shift(r,-i))
        permutations.append(tmp_perms)
    #print(permutations)
    combinations = list(itertools.product(*permutations))
    #print(combinations)

    for l in combinations:
            patterns_founds=find_patterns(l)
            for p in patterns_founds:
                counts_patterns_encountered[p]+=1

    coefficients = np.array([])
    for key, value in counts_patterns_encountered.items():
        counts_patterns_encountered[key] = value/(3**num_traits) #Divide by the number of shares to get the expected values
        #print(counts_combinations_encountered[key])
        coefficients = np.append(coefficients, counts_patterns_encountered[key]) #Convert to numpy array
    return(coefficients)


def compute_T_inv(num_shares, num_traits):
    from numpy.linalg import inv
    T = []

    possible_variables_combinations = list(itertools.product([0, 1], repeat=num_traits)) #AnB, AnnotB, notAnB, notAnnotB

    for c in possible_variables_combinations:
        #print(c)
        tmp_shares = []
        for e in c:
            if e == 1:
                tmp_shares.append([1,1,0])
            elif e == 0:
                tmp_shares.append([1,0,0])
        #print(tmp_shares)
        tmp_exp = compute_expected_values(tmp_shares, num_traits)
        T.append(tmp_exp)

    T = np.matrix(T)
    #print(T)
    T_inv = inv(T)
    #print(T_inv)
    return T_inv


def all_patterns_count(dataset):
    possible_patterns = list(itertools.product([0, 1], repeat=len(dataset[0]))) #AnB, AnnotB, notAnB, notAnnotB
    counts = []
    for p in possible_patterns:
        counts.append(pattern_count(dataset,p))
    return(counts)


def pattern_count(dataset, pattern=[]):
    count = 0
    for i in range(len(dataset)):
        match = True
        for ind in range(len(dataset[0])):
            if dataset[i][ind]!=pattern[ind]:
                match=False
        if match:
            count+=1

    return count


def split_and_compute(ds):
    ds_split = split_dataset(ds)
    # print(ds_split)

    # conv_matrix = 1/3 * np.matrix([ [4.0, -2, -2, 1],
    #                                [-2, 4, 1, -2],
    #                                [-2, 1, 4, -2],
    #                                [1, -2, -2, 4]])
    # print(conv_matrix)


    # count_original_11 = pattern_count(ds, lst_traits, [1,1])
    # count_original_10 = pattern_count(ds, lst_traits, [1,0])
    # count_original_01 = pattern_count(ds, lst_traits, [0,1])
    # count_original_00 = pattern_count(ds, lst_traits, [0,0])


    # ratio_10 = count_original_10/nu
    # ratio_01 = count_original_01/nu
    # ratio_00 = count_original_00/nu

    # count_split_11 = pattern_count(ds_split, lst_traits, [1,1])
    # count_split_10 = pattern_count(ds_split, lst_traits, [1,0])
    # count_split_01 = pattern_count(ds_split, lst_traits, [0,1])
    # count_split_00 = pattern_count(ds_split, lst_traits, [0,0])


    counts_original = all_patterns_count(ds)
    counts_split = all_patterns_count(ds_split)
    return (ds_split, counts_original, counts_split)


'''
def full_col_count(dataset, lst_trait_indces=[], lowerlimit = -1, upperlimit=-1):

    if lowerlimit == -1:
        lowerlimit = 0

    if upperlimit == -1:
        upperlimit = len(dataset)

    count = 0
    for i in range(lowerlimit, upperlimit):
        if is_user_positive(dataset[i],lst_trait_indces):
            count += 1

    return count# / len(dataset)
    # print(ratio)



def prob_no_column(traits):
    if traits == 1:
        print("Error: Traits <2.")
    elif traits == 2:
        return (2.0/3.0)*(1.0/3.0)
    else:
        sum = 0
        for i in range(traits-2):
            sum += (((2.0/3.0)**(traits-2))/(2**i))

        return (prob_no_column(traits-1) + (sum * (2.0/3.0)*(1.0/3.0)))
'''


########################################################################

num_shares = shares
gen_dataset = 1


lst_of_proportions = ['0.1','0.3','0.5','0.7']

lst_lst_traits = []
lst_lst_traits.append(['F0','F2','F4','F5','F9'])
lst_lst_traits.append(['F0','F2','F4','F5','F6'])
lst_lst_traits.append(['F2','F4','F5','F6','F9'])
lst_lst_traits.append(['F2','F4','F5','F6','F7'])


for index,lst_traits in enumerate(lst_lst_traits):
    items = lst_traits
    print(items)

    ds = {}
    raw_data = open('../datasets/synthetic/varying_traits/0.99_tsz10_tct100.0k.txt')
    for i, line in enumerate(raw_data):
        tmp_record = {}

        #Initialize
        for item in items:
            tmp_record[items.index(item)] = 0

        #Add elements
        for item in line.split(" "):
            if item in items:
                tmp_record[items.index(item)] = 1

        ds[i] = tmp_record
    nu = len(ds)
    num_traits = len(ds[0])
    #print(nu)
    raw_data.close()

    #print(ds)


    print("\n\n====================== Experiment Params ==================================")
    print("Shares               : " + str(shares))
    print("Users                : " + str(nu))
    # print("Positive Users       : " + str(positive_nu))
    # print("Negative Users       : " + str(negative_nu))
    # print("Ratio                : " + str(ratio))
    print("Traits               : " + str(lst_traits))
    print("===========================================================================\n")

    #    print("====================== Dataset Details ====================================")
    #    print("Original Dataset Size        : " + str(len(ds)))
    #    print("Split Dataset Size           : " + str(len(ds_split)))
    #    print("===========================================================================\n\n")


    for iter in range(100): #Experiment repeat
        (ds_split, counts_original, counts_split) = split_and_compute(ds)


        counts_split_vec = np.array(counts_split).reshape((-1, 1)) #Transpose
        #print(counts_split_vec)
        #print(counts_original)
        #print(counts_split)
        #counts_split = list(reversed(counts_split))
        #print(counts_split)

        conv_matrix = compute_T_inv(num_shares, num_traits)
        #print("---------")
        #print(conv_matrix)
        estimates = (conv_matrix*counts_split_vec).tolist()
        #print("---------")
        #print(estimates)
        #print("---------")
        estimate_num_X_and_Y = estimates[2**num_traits-1][0]
        estimate_ratio_X_and_Y = estimates[2**num_traits-1][0]/nu

        estimate_num_X_and_not_Y = estimates[2**num_traits-2][0]
        estimate_ratio_X_and_not_Y = estimates[2**num_traits-2][0]/nu


        ################## GroundTruth
        observations = [[] for t in range(num_traits-1)]
        for i in range(nu):  # For each user
            for t in range(num_traits-1):
                observations[t].append(ds[i][t])

        cand_vect =[]
        for i in range(nu):
            cand_vect.append(ds[i][num_traits-1])

        rules_orig = association_rules(observations, cand_vect, num_shares=1)


        ################## Evaluation
        observations = [[] for t in range(num_traits-1)]
        for i in range(nu*num_shares):  # For each split
            for t in range(num_traits-1):
                observations[t].append(ds_split[i][t])

        cand_vect =[]
        for i in range(nu*num_shares):
            cand_vect.append(ds_split[i][num_traits-1])

        rules_split = association_rules(observations, cand_vect, num_shares=num_shares, num_X_and_not_Y=estimate_num_X_and_not_Y , num_X_and_Y=estimate_num_X_and_Y)

        support_err    = ((abs(rules_split[2]-rules_orig[2])/float(rules_orig[2]))*100)
        confidence_err = ((abs(rules_split[3]-rules_orig[3])/float(rules_orig[3]))*100)
        lift_err       = ((abs(rules_split[4]-rules_orig[4])/float(rules_orig[4]))*100)

        print("Iteration: " + str(iter))
        print("Support Inters.(Percent Error)        : " + str(support_err) + "%")
        print("Confidence     (Percent Error)        : " + str(confidence_err) + "%")
        print("Lift           (Percent Error)        : " + str(lift_err) + "%")
        with open("../results//num_of_traits//" + '-'.join(lst_traits)+"_5.csv", "a+") as results:
            print(','.join([str(counts_original[-1]), str(iter), str(support_err), str(confidence_err), str(lift_err)]))
            results.write(','.join([str(counts_original[-1]), lst_of_proportions[index], '-'.join(lst_traits), str(iter), str(support_err), str(confidence_err), str(lift_err)])+"\n")

    ##################
    #trait_percent_original = trait_percent(ds, lst_traits, 1)
    #trait_percent_split = trait_percent(ds_split, lst_traits, num_shares)
    #strait_corr = correlation_stat(ds, lst_traits)
    #trait_corr = correlation_stat(ds_split, lst_traits)

    '''
    print("========================= Intermediate Values =============================")
    #print("Ratio                              : " + str(ratio))
    print("Ratio Estimate                     : " + str(estimate_ratio_X_and_Y))
    print("Groundtruth                        : " + str(counts_original[-1]))
    print("Estimate                           : " + str(estimate_num_X_and_Y))
    print("Percent ratio )                    : " + str((float((abs(estimate_num_X_and_Y-counts_original[-1]))/counts_original[-1])*100)) + "%")
    print(" ")
    
    
    
    print("========================= Results =========================================")
    print("Original Dataset")
    print("SupportX                              : " + str(rules_orig[0]))
    print("SupportY                              : " + str(rules_orig[1]))
    print("Support Intersection                  : " + str(rules_orig[2]))
    print("Confidence                            : " + str(rules_orig[3]))
    print("Lift                                  : " + str(rules_orig[4]))
    #print("Conviction                            : " + str(rules_orig[5]))
    print("------")
    print("Split Dataset")
    print("SupportX                              : " + str(rules_split[0]))
    print("SupportY                              : " + str(rules_split[1]))
    print("Support Intersection                  : " + str(rules_split[2]))
    print("Confidence                            : " + str(rules_split[3]))
    print("Lift                                  : " + str(rules_split[4]))
    #print("Conviction                            : " + str(rules_split[5]))
    print("------")
    print("SupportX (Percent Error)              : " + str((abs(rules_split[0]-rules_orig[0])/rules_orig[0])*100) + "%")
    print("SupportY (Percent Error)              : " + str((abs(rules_split[1]-rules_orig[1])/rules_orig[1])*100) + "%")
    print("Support Inters.(Percent Error)        : " + str((abs(rules_split[2]-rules_orig[2])/rules_orig[2])*100) + "%")
    print("Confidence     (Percent Error)        : " + str((abs(rules_split[3]-rules_orig[3])/rules_orig[3])*100) + "%")
    print("Lift           (Percent Error)        : " + str((abs(rules_split[4]-rules_orig[4])/rules_orig[4])*100) + "%")
    #print("Conviction     (Percent Error)        : " + str((abs(rules_split[5]-rules_orig[5])/rules_orig[5])*100) + "%")
    
    #print("Estimated Positives                    : " + str(expected_PI_positives))
    #print("Estimated Negatives                    : " + str(expected_PI_negatives))
    #print("Percent ratio (True Est.)             : " + str(math.ceil(float((abs(estimated_PI_ratio-ratio))/ratio)*100)) + "%")
    #print("Error Percent (True Est.)             : " + str(math.ceil(float((abs(estimated_PI_ratio-ratio)))*100)) + "%")
    print("===========================================================================\n\n")
    '''



    '''
    print("10 Ratio                              : " + str(ratio_10))
    print("10 Ratio Estimate                     : " + str(estimate_ratio_10))
    print("Groundtruth #10                       : " + str(ratio_10*nu))
    print("Estimate 10                           : " + str(estimate_num_10))
    print("Percent ratio (10)                    : " + str((float((abs(estimate_ratio_10-ratio_10))/ratio_10)*100)) + "%")
    print(" ")
    print("01 Ratio                              : " + str(ratio_01))
    print("01 Ratio Estimate                     : " + str(estimate_ratio_01))
    print("Groundtruth #01                       : " + str(ratio_01*nu))
    print("Estimate 01                           : " + str(estimate_num_01))
    print("Percent ratio (01)                    : " + str((float((abs(estimate_ratio_01-ratio_01))/ratio_01)*100)) + "%")
    print(" ")
    print("00 Ratio                              : " + str(ratio_00))
    print("00 Ratio Estimate                     : " + str(estimate_ratio_00))
    print("Groundtruth #00                       : " + str(ratio_00*nu))
    print("Estimate 00                           : " + str(estimate_num_00))
    print("Percent ratio (00)                    : " + str((float((abs(estimate_ratio_00-ratio_00))/ratio_00)*100)) + "%")
    print(" ")
    #print("If independent uniformly distr. events: " + str(0.5**len(lst_traits)))
    #print("Positives Orig                           : " + str(count_original))
    #print("Total Columns in split dataset            : " + str(count_split))
    #print("Positives Estimated                       : " + str(estimate_positive_nu_PI))
    #print("Percent ratio (Total)                    : " + str(math.ceil(float(abs(count_split-expected_count_PI))/float(count_split)*100)) + "%")
    
    print("")
    #print("Count Total                               : " + str(count_positives+count_negatives))
    #print("Count Positives                           : " + str(count_positives))
    #print("Expected Count Positives                  : " + str(expected_count_PI_positives))
    #print("Percent ratio (Positives)                 : " + str(math.ceil(float(abs(count_positives-expected_count_PI_positives))/float(count_positives)*100)) + "%")
    print("")
    #print("Count Negatives                            : " + str(count_negatives))
    #print("Expected Count Negatives                   : " + str(expected_count_PI_negatives))
    #print("Percent ratio (Negatives)                 : " + str(math.ceil(float(abs(count_negatives-expected_count_PI_negatives))/float(count_negatives)*100)) + "%")
    
    print("")
    #print("Pr[ 1 column | negative]                  : " + str(pr_negatives_one_column))
    #print("Pr[zero columns | positive]               : " + str(pr_positive_zero_columns))
    #print("Pr[only 1 column | positive]              : " + str(pr_positive_only_one_column))
    #print("Pr[two columns | positive]                : " + str(pr_positive_two_columns))
    #print("Pr[one or two columns | positive]         : " + str(pr_positive_two_columns+pr_positive_only_one_column))
    #print("Pr[one or (2X) two columns | positive]    : " + str(2*pr_positive_two_columns+pr_positive_only_one_column))
    #print("Pr[positive at least 1 column] old       : " + str(pr_positive_1st_column+pr_positive_2nd_column*pr_positive_1st_column))
    #print("Pr[negative 1 column]                     : " + str(pr_negatives_one_column))
    #print("\# of negative patients forming col.]    : " + str(pr_negative_column*nu)
    '''

    print("===========================================================================\n\n")




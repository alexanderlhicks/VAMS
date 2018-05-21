import pandas

import matplotlib.pyplot as plt

data = pandas.read_csv('results//num_of_pos//merged.csv', sep=',', na_values='.')
numpos_data = data.groupby('counts')

data.boxplot(by='counts', column=['support_err'])
#plt.ylim(0, 100)
plt.xlabel("Rule Occurrences")
plt.ylabel("Percent Error")
#plt.title("Support")
plt.title("")
plt.suptitle("") #Remove pandas title
plt.savefig("results//num_of_pos//plots//support.pdf", bbox_inches='tight')
plt.show()


data.boxplot(by='counts', column=['lift_err'])


#plt.ylim(0, 100)
plt.xlabel("Rule Occurrences", fontsize=13)
plt.ylabel("Percent Error", fontsize=13)
#plt.title("Lift", fontsize=14)
plt.title("")
plt.suptitle("") #Remove pandas title
plt.savefig("results//num_of_pos//plots//lift.pdf", bbox_inches='tight')
plt.show()


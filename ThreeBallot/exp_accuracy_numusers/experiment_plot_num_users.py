import pandas

import matplotlib.pyplot as plt


data_1000 = pandas.read_csv('../results//num_of_users//merged_1000.csv', sep=',', na_values='.')
data_10000 = pandas.read_csv('../results//num_of_users//merged_10000.csv', sep=',', na_values='.')
data_100000 = pandas.read_csv('../results//num_of_users//merged_100000.csv', sep=',', na_values='.')
data_1000000 = pandas.read_csv('../results//num_of_users//merged_1000000.csv', sep=',', na_values='.')
#numpos_data = data.groupby('proportion')
#x_y_df = data[['proportion','support_err']]

#with pandas.option_context('display.max_rows', None, 'display.max_columns', 3):
#    print(x_y_df)

#Support
#data.boxplot(by='proportion', column=['support_err'])
median_df = data_1000.groupby('proportion', as_index=False).median()
ax = median_df.plot(x='proportion', y='support_err')

median_df = data_10000.groupby('proportion', as_index=False).median()
median_df.plot(x='proportion', y='support_err', ax=ax)

median_df = data_100000.groupby('proportion', as_index=False).median()
median_df.plot(x='proportion', y='support_err', ax=ax)

median_df = data_1000000.groupby('proportion', as_index=False).median()
median_df.plot(x='proportion', y='support_err', ax=ax)

#plt.ylim(0, 100)
plt.xlabel("Support")
plt.ylabel("Percent Error")
#plt.title("Support")
plt.title("")
plt.suptitle("") #Remove pandas title

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ["1000 Records", "10000 Records", "100000 Records", "1M Records"])

plt.savefig("../results//num_of_users//plots//support.pdf", bbox_inches='tight')
plt.show()

'''
#Lift
data.boxplot(by='proportion', column=['lift_err'])
#plt.ylim(0, 100)
plt.xlabel("Rule Occurrences", fontsize=13)
plt.ylabel("Percent Error", fontsize=13)
#plt.title("Lift", fontsize=14)
plt.title("")
plt.suptitle("") #Remove pandas title
plt.savefig("../results//num_of_users//plots//lift.pdf", bbox_inches='tight')
plt.show()
'''

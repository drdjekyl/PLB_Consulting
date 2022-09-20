import pandas as pd
import glob
import os

path = r'russian-troll-tweets-master' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

li = []
print(all_files)

for filename in all_files:
    
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

dfs = pd.concat(li, axis=0, ignore_index=True)

print(dfs.info())

# EXTRACT TOP 5 AUTHORS BY NUMBER OF TWEETS
dfs_author = {}
for value in dfs.author:
    if value not in dfs_author.keys():
        dfs_author[value] = 1
        
    else:
        dfs_author[value] = dfs_author[value] + 1
        
top_5 = sorted(dfs_author, key=dfs_author.get, reverse=True)[:5]

print('Highest tweet numbers for TOP 5 authors')
for k in top_5:
    print(k, dfs_author[k])

# SELECT TWEETS WRITTEN THE 2016 JAN, 1ST
for idx, date in zip(dfs.index, dfs.publish_date):
    dfs.loc[idx, 'publish_date'] = pd.Timestamp(date)
    
jan_first = dfs[(dfs.publish_date > pd.Timestamp('2016-01-01')) & (
    dfs.publish_date < pd.Timestamp('2016-01-02'))]

# WRITE TWEETS SELECTED INTO CSV FILE
jan_first_csv = jan_first.to_csv()
with open('tweet_jan_1st.csv', 'w') as file:
    file.write(jan_first_csv)

# FORMAT ID AS TYPE FLOAT
column_id = [col for col in dfs.columns if col.endswith('id')]

for col in dfs.loc[:, column_id]:
    for idx, value in zip(dfs[col].index, dfs[col]):
        
        try:
            
            value = float(value) 
            
        except ValueError:
            
            value = np.nan
            
        dfs.loc[idx, col] = value
                                          
dfs.loc[:, column_id].astype(float)

"""READ CSV, EXTRACT INFOS AND DUMP TO JSON"""

import pandas as pd
import numpy as np
import multiprocessing as mp
from pathos.multiprocessing import ProcessingPool as Pool
import glob
import os
import time 

def time_decorator(func): 
    def wrapper(*args): 
        clock = time.time()
        ret = func(*args)
        elapsed = time.time() - clock
        print(f"[{func}]: Time elapsed {elapsed} s") 
    
        return ret 

    return wrapper 

@time_decorator
def load_data():
    path = r'../../data/russian-troll-tweets-master' # use your path
    all_files = glob.glob(os.path.join(path, "*.csv"))
    print(all_files)
    
    
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        li.append(df)

    dfs = pd.concat(li, axis=0, ignore_index=True)

    return dfs

@time_decorator
def select_tweet(dfs):
    jan_first = dfs.publish_date.apply(lambda x: x.startswith('1/1/2016'))
    
    """
    dfs.publish_date = dfs.publish_date.apply(lambda date: pd.Timestamp(date))

    jan_first = dfs[(dfs.publish_date > pd.Timestamp('2016-01-01')) & (
        dfs.publish_date < pd.Timestamp('2016-01-02'))]
    """

    return jan_first

@time_decorator
def tweet_selected_to_csv(jan_first):
    jan_first_csv = jan_first.to_csv()
    
    with open('tweet_jan_1st.csv', 'w') as file:
        file.write(jan_first_csv)

def para_ids(dfs_):
    for col in dfs_.loc[:, column_id]:
        
        for idx, value in zip(dfs_[col].index, dfs_[col]):
            try:
                value = float(value) 

            except ValueError:
                value = np.nan

            dfs_.loc[idx, col] = value
    
    return dfs_

@time_decorator
def apply_para_ids(dfs):
    cores = mp.cpu_count()
    pool = Pool(cores)

    df_split = np.array_split(dfs.loc[:, column_id], cores, axis=0)
    df_out = np.vstack(pool.map(para_ids, df_split))
    
    return df_out

if __name__ == '__main__':
    
    print(30*'_')
    print('LOAD DATA IN A DATAFRAME')
    dfs = load_data()
    print(dfs.info())

    print(30*'_')
    print('EXTRACT TOP 5 AUTHORS BY NUMBER OF TWEETS')
    print(dfs.author.value_counts().head(5))

    print(30*'_')
    print('SELECT TWEETS WRITTEN THE 2016 JAN, 1ST')
    jan_first = select_tweet(dfs)

    print(30*'_')
    print('WRITE THEM INTO CSV FILE')
    tweet_selected_to_csv(jan_first)

    print(30*'_')
    print('FORMAT ID COLUMNS AS TYPE FLOAT')
    column_id = [col for col in dfs.columns if col.endswith('id')]

    print(30*'_')
    print('USE POOL TO PARALLEL TASK IN PARA IDS')
    df_out = apply_para_ids(dfs)
    print(df_out)

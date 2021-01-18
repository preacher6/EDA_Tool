import pandas as pd 
import numpy as np 
  
nums = {'Number_set_1': [0, 1, 1, 2, 3, 5, np.nan, 
                         13, 21, np.nan], 
       'Number_set_2': [3, 7, np.nan, 23, 31, 41,  
                        np.nan, 59, 67, np.nan], 
       'Number_set_3': [2, 3, 5, np.nan, 11, 13, 17, 
                        19, 23, np.nan]} 
  
# Create the dataframe 
df = pd.DataFrame(nums) 
  
# Apply the function 
df[['Number_set_2', 'Number_set_1']] = df[['Number_set_2', 'Number_set_1']].fillna(0)
df.drop(df.index[0:4], inplace=True)
print(df)
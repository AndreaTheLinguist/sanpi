# coding=utf-8
import pandas as pd

def balance_sample(full_df: pd.DataFrame(), 
                   column_name: str, 
                   sample_per_value: int = 5, 
                   verbose: bool = False):
    '''
    create sample with no more than n rows satisfying each unique value of the given column. A value of 0 for `sample_per_value` will limit all values' results to the minimum count per value.
    '''
    sub_samples = []
    n = 5 if not sample_per_value else sample_per_value
    
    for c in full_df.loc[:, column_name].unique():
        sdf = full_df.loc[full_df[column_name] == c, :].sample(min(full_df.value_counts(subset=column_name)[c], n))
        sub_samples.append(sdf)
    if not sample_per_value: 
        trim_len = min(len(sdf) for sdf in sub_samples)
        sub_samples = [sdf.iloc[:trim_len, :] 
                       for sdf in sub_samples]
    b_sample = pd.concat(sub_samples)
    if verbose:
        subset_info = b_sample.value_counts(subset=column_name).to_frame(name='count').assign(percentage=b_sample.value_counts(column_name, normalize=True).round(2) * 100).to_markdown()
        
        return (b_sample, 
                f'\n## {column_name} representation in sample:\n{subset_info}')
    else: 
        return b_sample
    
def cols_by_str(df:pd.DataFrame(), start_str:str='dep'):
    return df.columns[df.columns.str.startswith(start_str)].to_list()

def make_cats(df):
    cat_suff = ("code", "name", "path", "stem")
    cat_cols = df.columns.str.endswith(cat_suff)
    df.loc[:, cat_cols] = df.loc[:, cat_cols].astype('string').astype('category')
    return df
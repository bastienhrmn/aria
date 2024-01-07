import pandas as pd

def data_explo(path_file):
    """
    Short EDA function to better understand the dataset.
    :parma str path_file: path of the csv file to explore.
    """
    print('Exporing file : {}'.format(path_file))
    data_input = pd.read_csv(path_file,
                             sep=';',
                             decimal=',')
    # we set the display to all columns for the dataframe
    pd.set_option('display.max_columns', None)
    print(data_input.head(5))
    print('-----------')
    print(data_input.info())

    return data_input


def show_df_loans(df_with_all_loans):
    """
    Exploratory data analysis to understand how many loans are concerned in the study.
    """
    print('========================')
    no_trust = df_with_all_loans[df_with_all_loans['trustId'].isna()]
    print(no_trust.info())
    print('========================')
    eligible_criteria = no_trust[no_trust['status'].isin(['ACCEPTED', 'TO_REPAY'])]
    print(eligible_criteria.info())
    print('========================')
    eligible_criteria = eligible_criteria[eligible_criteria['currency'] == 'EUR']
    print(eligible_criteria.info())
    print(eligible_criteria.head(5))
from eda import data_explo, show_df_loans
from loan_allocation import get_metrics_portfolio, allocation_of_loans


def main():
    # let's explore the input dataset, which is the dataset with all the loans
    df_with_all_loans = data_explo(path_file='data/data-engineering_exercise.csv')

    # let's explore the input data
    # show_df_loans(df_with_all_loans)
    """
    it shows that we have 3139 loans, in which only 2500 have a trustId
    after the EDA, we find 639 loans with no trust
    in these 639, 136 are in the eligibility criterias
    """

    # let's explore the portfolio's health before allocating new loans
    # new_loan = df_with_all_loans[df_with_all_loans['trustId'].isna()].iloc[[0]]
    # print(get_metrics_portfolio('db0d8688-9496-405b-b853-96bdcd4fa630',
    #                       df_with_all_loans,
    #                       new_loan))
    # print(get_metrics_portfolio('9f5a726c-6708-4124-a9a0-5e8c22383e84',
    #                       df_with_all_loans,
    #                       new_loan))
    # print(get_metrics_portfolio('4bb872a9-657b-4d61-9158-bc42983bdb0c',
    #                       df_with_all_loans,
    #                       new_loan))
    """
    Portfolio db0d8688-9496-405b-b853-96bdcd4fa630 is near its amount threshold.
    Portfolio 9f5a726c-6708-4124-a9a0-5e8c22383e84 is near its biggest owner threshold and insurance rate threshold.
    Portfolio 4bb872a9-657b-4d61-9158-bc42983bdb0c is near its foreign loans and already surpassed its max owner threshold.
    """


    # let's allocate the loans with no trustId and that meets the eligibility criteria
    allocation_of_loans(df_with_all_loans=df_with_all_loans)
    """
    We allocate only 23 loans, and only to the db0d8688-9496-405b-b853-96bdcd4fa630 portfolio
    """    


if __name__ == '__main__':
    main()
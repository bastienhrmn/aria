import pandas as pd
from metrics_covenant import compute_covenants_portfolio

def get_metrics_portfolio(portfolio_id,
                          df_with_all_loans,
                          new_loan):
    """
    Get the metrics of the covenants of a portfolio, and the new ones with the new loan.
    :param str portfolio_id: one of the three portfolio id
    :param dataframe df_with_all_loans: dataame with all the loans of the project
    :param dataframe new_loan: a one line dataframe with the new loan to potentially add to the portfolio.
    """
    # check if the portfolio id exists
    if portfolio_id not in ['db0d8688-9496-405b-b853-96bdcd4fa630',
                            '9f5a726c-6708-4124-a9a0-5e8c22383e84',
                            '4bb872a9-657b-4d61-9158-bc42983bdb0c']:
        raise Exception('Portfolio Id does not exists !')
    
    # we focus on the loans of the portfolio in the parameter
    loans_of_specific_portfolio = df_with_all_loans[
        df_with_all_loans['trustId'] == portfolio_id]
    
    # then, we measure the different metrics of the covenants
    portfolio_weight_biggest_owner, portfolio_insurance_rate, portfolio_weight_foreign_loans, portfolio_amount = compute_covenants_portfolio(loans_of_specific_portfolio)

    # now we simulate all those same metrics if we added the new loan to this portfolio
    loans_of_specific_portfolio_with_new_loan = pd.concat([loans_of_specific_portfolio, new_loan], ignore_index=True)

    # now we simulate the new metrics of the covenants if we add the new loan
    new_portfolio_weight_biggest_owner, new_portfolio_insurance_rate, new_portfolio_weight_foreign_loans, new_portfolio_amount = compute_covenants_portfolio(loans_of_specific_portfolio_with_new_loan)

    dict_rep = {'portfolio_id': portfolio_id,
                'portfolio_weight_biggest_owner': portfolio_weight_biggest_owner,
                'portfolio_insurance_rate': portfolio_insurance_rate,
                'portfolio_weight_foreign_loans': portfolio_weight_foreign_loans,
                'portfolio_amount': portfolio_amount,
                'new_portfolio_weight_biggest_owner': new_portfolio_weight_biggest_owner,
                'new_portfolio_insurance_rate': new_portfolio_insurance_rate,
                'new_portfolio_weight_foreign_loans': new_portfolio_weight_foreign_loans,
                'new_portfolio_amount': new_portfolio_amount}
    
    return dict_rep


def is_breaking_covenant(metrics_portfolio):
    """
    Return if the new loan to add is ok or is breaking one of the covenant.
    :param metrics_portfolio: the result of the get_metrics_portfolio function.
    """
    portfolio_id = metrics_portfolio.get('portfolio_id')
    if portfolio_id == 'db0d8688-9496-405b-b853-96bdcd4fa630':
        threshold = {'max_weight_single_owner': 1,
                     'min_portfolio_insurance_rate': 0.5,
                     'max_weight_foreign_loans': 0.4,
                     'max_portfolio_amount': 800000}
    elif portfolio_id == '9f5a726c-6708-4124-a9a0-5e8c22383e84':
        threshold = {'max_weight_single_owner': 0.4,
                     'min_portfolio_insurance_rate': 0.7,
                     'max_weight_foreign_loans': 1,
                     'max_portfolio_amount': 400000}
    elif portfolio_id == '4bb872a9-657b-4d61-9158-bc42983bdb0c':
        threshold = {'max_weight_single_owner': 0.15,
                     'min_portfolio_insurance_rate': 0.6,
                     'max_weight_foreign_loans': 0.35,
                     'max_portfolio_amount': 1200000}
    else:
        raise Exception('Portfolio Id does not exists !')
    
    # get the new metrics of the covenants with the new potential loan
    new_portfolio_weight_biggest_owner = metrics_portfolio.get('new_portfolio_weight_biggest_owner')
    new_portfolio_insurance_rate = metrics_portfolio.get('new_portfolio_insurance_rate')
    new_portfolio_weight_foreign_loans = metrics_portfolio.get('new_portfolio_weight_foreign_loans')
    new_portfolio_amount = metrics_portfolio.get('new_portfolio_amount')

    # chekc if the new loan is above the different threshold of the given portfolio
    if new_portfolio_weight_biggest_owner <= threshold.get('max_weight_single_owner') and \
        new_portfolio_insurance_rate >= threshold.get('min_portfolio_insurance_rate') and \
            new_portfolio_weight_foreign_loans <= threshold.get('max_weight_foreign_loans') and \
                new_portfolio_amount <= threshold.get('max_portfolio_amount'):
        breaking_covenant = False
    else:
        breaking_covenant = True
    
    return breaking_covenant


def go_no_go_specific_loan(df_with_all_loans,
                           index,
                           trust_id):
    """
    Allocate the loan if it is eligible and meets all the criterias of the threshold.
    :param dataframe df_with_all_loans: dataframe with all the loans
    :param int index: index of the row of the loan with no trust we are studying.
    :param str trust_id: portfolio id we're trying to add the loan to.
    """
    loan_allocated = False
    # if the loan is eligible (no trust + eligibility criterias)
    if isinstance(df_with_all_loans.loc[index]['trustId'], float) and \
            df_with_all_loans.loc[index]['status'] in ['ACCEPTED', 'TO_REPAY'] and \
                df_with_all_loans.loc[index]['currency'] == 'EUR':
            
            # spot the loan we are studying
            new_loan = df_with_all_loans[df_with_all_loans['trustId'].isna()].loc[[index]]

            # get the metrics if we add the loan to the specific portfolio
            metrics_new_loan = get_metrics_portfolio(portfolio_id=trust_id,
                                                        df_with_all_loans=df_with_all_loans,
                                                        new_loan=new_loan)
            
            # if we do not break any covenant, we add the loan to the portfolio
            if not is_breaking_covenant(metrics_new_loan):
                print('-------')
                print('Loan with index {} and id {} allocated to trust {} '.format(index,
                                                                                   df_with_all_loans.loc[index]['id'],
                                                                                   trust_id))
                # print(metrics_new_loan)
                df_with_all_loans.at[index, 'trustId'] = trust_id
                
                # stop the function as soon as we can allocate the specific loan
                loan_allocated = True
            else:
                pass
    
    return loan_allocated


def allocation_of_loans(df_with_all_loans):
    """
    Allocate the loan to the first portfolio that meets all critertias.
    :param dataframe df_with_all_loans: dataframe with all the loans
    """
    # we try to allocate the loan to trusts in the allocation priority order for trusts
    trust_allocation_priority = ['db0d8688-9496-405b-b853-96bdcd4fa630',
                                 '9f5a726c-6708-4124-a9a0-5e8c22383e84',
                                 '4bb872a9-657b-4d61-9158-bc42983bdb0c']
    
    for index, row in df_with_all_loans.iterrows():
        # if the loan is not allocated yet to a portfolio, we work to allocate it
        # we also check the eligibility criteria of the loan to be allocated
        for trust_id in trust_allocation_priority:
            loan_allocated = go_no_go_specific_loan(df_with_all_loans=df_with_all_loans,
                                                    index=index,
                                                    trust_id=trust_id)
            # we stop the allocation as soon as we allocate the loan
            if loan_allocated:
                break
            else:
                pass
        
    df_with_all_loans.to_csv('output/output_dataset.csv', sep=';')
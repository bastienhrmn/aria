def compute_portfolio_biggest_single_user_weight(loans_of_specific_portfolio):
    """
    Compute the weight of the biggest owner
    """
    current_amount_of_loans = loans_of_specific_portfolio['amount'].sum()
    # sum of amount per client
    current_number_of_foreign_loans = loans_of_specific_portfolio.groupby('ownerId')['amount'].sum()

    # taking the owner with maximum amount (unused for now)
    biggest_owner_id = current_number_of_foreign_loans.idxmax()
    # computing the weight of this specific client on the portfolio
    amount_biggest_owner = current_number_of_foreign_loans.max()
    portfolio_weight_biggest_owner = amount_biggest_owner / current_amount_of_loans
    return portfolio_weight_biggest_owner


def compute_portfolio_insurance_rate(loans_of_specific_portfolio):
    """
    Compute the insurance rate
    """
    current_number_of_loans = len(loans_of_specific_portfolio)
    current_number_of_insured_loans = len(loans_of_specific_portfolio[loans_of_specific_portfolio['insuranceStatus'] == 'ACTIVATED'])
    portfolio_insurance_rate = current_number_of_insured_loans / current_number_of_loans
    return portfolio_insurance_rate


def compute_portfolio_weight_of_foreign_loans(loans_of_specific_portfolio):
    """
    Compute the weight of foreign loans
    """
    current_amount_of_loans = loans_of_specific_portfolio['amount'].sum()
    current_amount_of_foreign_loans = loans_of_specific_portfolio[loans_of_specific_portfolio['country'] != 'FR']['amount'].sum()
    portfolio_weight_foreign_loans = current_amount_of_foreign_loans / current_amount_of_loans
    return portfolio_weight_foreign_loans


def compute_portfolio_amount(loans_of_specific_portfolio):
    """
    Compute the amount of a portfolio
    """
    return loans_of_specific_portfolio['amount'].sum()


def compute_covenants_portfolio(loans_of_specific_portfolio):
    """
    Copute all the metrics of a portfolio
    """
    # computing the weight of the biggest owner
    portfolio_weight_biggest_owner = compute_portfolio_biggest_single_user_weight(loans_of_specific_portfolio)

    # computing the portfolio insurance rate
    portfolio_insurance_rate = compute_portfolio_insurance_rate(loans_of_specific_portfolio)

    # computing the weight of foreign loans
    portfolio_weight_foreign_loans = compute_portfolio_weight_of_foreign_loans(loans_of_specific_portfolio)

    # computing the total amount of the portfolio
    portfolio_amount = compute_portfolio_amount(loans_of_specific_portfolio)

    return portfolio_weight_biggest_owner, portfolio_insurance_rate, portfolio_weight_foreign_loans, portfolio_amount
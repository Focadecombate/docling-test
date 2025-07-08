read_expenses = """
Please convert the following markdown invoice data into a structured JSON format following these specifications:

Create a root object called 'fatura' with two main sections: 'metadata' and 'expenses'
For the metadata section:

Parse the date_of_emission as a string
Parse the total_amount as a number, converting from Brazilian format (remove dots and replace comma with period)


For the expenses section, create arrays for:

current_expenses: entries from the first table
installments: entries from the second table
international_transactions: entries from the third table
future_payments: entries from the fourth table


For each expense entry in the tables:

Keep DATA as 'date'
Keep ESTABELECIMENTO as 'establishment'
Convert VALOR (value) from Brazilian currency format to number
Handle empty or missing values as null
Preserve any negative values (marked with minus sign)


For special cases:

Group international transaction details (conversion rate, IOF) under the international_transactions object
Include summary totals for future payments as separate properties
Only include International transactions if there is a IOF charge


The output should be only the properly formatted JSON with all values properly typed (strings for text, numbers for amounts).
Expected structure:
{
'fatura': {
'metadata': {
'date_of_emission': string,
'total_amount': number
},
'expenses': {
'current_expenses': [{date, establishment, value}],
'installments': [{date, establishment, value}],
'international_transactions': {
'transactions': [{date, establishment, value}],
'conversion_rate': number,
'iof': number
},
'future_payments': {
'entries': [{date, establishment, value}],
'next_bill_total': number,
'other_bills_total': number,
'total_future_payments': number
}
}
}
}
"""

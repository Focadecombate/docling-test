import datetime

from pydantic import BaseModel


class Records(BaseModel):
    data: str
    establishment: str
    amount: float


class InternationalTransactions(BaseModel):
    transactions: list[Records]
    conversion_rate: float
    iof: float


class FuturePayments(BaseModel):
    entries: list[Records]
    next_bill_total: float
    other_bills_total: float
    total_future_payments: float


class Expenses(BaseModel):
    current_expenses: list[Records]
    installments: list[Records]
    international_transactions: InternationalTransactions
    future_payments: FuturePayments


class Metadata(BaseModel):
    date_of_emission: datetime.date
    total_amount: float


class Fatura(BaseModel):
    metadata: Metadata
    expenses: Expenses


class Result(BaseModel):
    fatura: dict

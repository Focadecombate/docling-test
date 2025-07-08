import datetime

from pydantic import BaseModel


class Records(BaseModel):
    date: str
    raw: str
    establishment: str | None = None
    description: str | None = None
    category: str | None = None
    amount: float


class InternationalTransactions(BaseModel):
    transactions: list[Records]
    conversion_rate: float | None = None
    iof: float | None = None


class FuturePayments(BaseModel):
    entries: list[Records]
    next_bill_total: float | None = None
    other_bills_total: float | None = None
    total_future_payments: float | None = None


class Expenses(BaseModel):
    current_expenses: list[Records]
    installments: list[Records]
    international_transactions: InternationalTransactions | None = None
    future_payments: FuturePayments | None = None


class Metadata(BaseModel):
    date_of_emission: datetime.date
    total_amount: float


class Fatura(BaseModel):
    metadata: Metadata
    expenses: Expenses


class Result(BaseModel):
    fatura: Fatura

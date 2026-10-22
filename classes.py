class Transaction:

    def __init__(self, date, type_, category, amount, description=''):
        self.date = date
        self.type_ = type_
        self.category = category
        self.amount = amount
        self.description = description

    def To_line(self):
        return f'{self.date},{self.type_},{self.category},{self.amount},{self.description}'


class FinanceManager:

    def __init__(self):
        self.transactions = []

    def Add(self, transaction):
        self.transactions.append(transaction)

    def Delete(self, index):
        if 0 <= index < len(self.transactions):
            self.transactions.pop(index)
            return True
        return False

    def Balance(self):
        income = 0
        expense = 0

        for t in self.transactions:
            if t.type_ == 'income':
                income += t.amount
            else:
                expense += t.amount

        return income - expense

    def Totals_by_category(self):
        Dict = {}

        for t in self.transactions:
            if t.type_ == 'expense':
                if t.category in Dict:
                    Dict[t.category] += t.amount
                else:
                    Dict[t.category] = t.amount

        return Dict
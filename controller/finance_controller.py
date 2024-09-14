from model.finance_model import add_transaction, get_transactions, delete_transaction, update_transaction, get_balance

class FinanceController:
    def __init__(self, view):
        self.view = view
        self.view.set_controller(self)

    def add_transaction(self, title, amount, is_expense):
        try:
            add_transaction(title, amount, is_expense)
            self.view.refresh_transactions()
            self.update_balance()
            self.view.show_message("Transação adicionada com sucesso!")
        except Exception as e:
            self.view.show_message(f"Erro ao adicionar transação: {e}")

    def get_transactions(self):
        try:
            return get_transactions()
        except Exception as e:
            self.view.show_message(f"Erro ao obter transações: {e}")
            return []

    def delete_transaction(self, transaction_id):
        try:
            delete_transaction(transaction_id)
            self.view.refresh_transactions()
            self.update_balance()
            self.view.show_message("Transação excluída com sucesso!")
        except Exception as e:
            self.view.show_message(f"Erro ao excluir transação: {e}")

    def update_transaction(self, transaction_id, title, amount, is_expense):
        try:
            update_transaction(transaction_id, title, amount, is_expense)
            self.view.refresh_transactions()
            self.update_balance() 
            self.view.show_message("Transação atualizada com sucesso!")
        except Exception as e:
            self.view.show_message(f"Erro ao atualizar transação: {e}")

    def get_balance(self):
        try:
            return get_balance()
        except Exception as e:
            self.view.show_message(f"Erro ao obter balanço: {e}")
            return 0, 0, 0  

    def update_balance(self):
        balance, expenses, income = self.get_balance()

        balance_text = f"Balanço: R$ {balance:.2f}"
        expense_text = f"Total de Despesas: R$ {expenses:.2f}"
        income_text = f"Total de Receitas: R$ {income:.2f}"

        if balance >= 0:
            balance_message = "Caminho certo de economizar!"
        else:
            balance_message = "Cuidado, você está no vermelho!"

        self.view.update_balance_labels(balance_text, expense_text, income_text, balance_message)

    def start_edit_transaction(self, transaction):
        self.view.show_edit_dialog(transaction)

    def save_edit_transaction(self, transaction_id):
        title = self.view.edit_title_input.value
        amount = float(self.view.edit_amount_input.value)
        is_expense = self.view.edit_is_expense_checkbox.value
        self.update_transaction(transaction_id, title, amount, is_expense)
        self.view.cancel_edit(None) 
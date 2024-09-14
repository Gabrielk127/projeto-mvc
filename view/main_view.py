import flet as ft

class MainView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.controller = None
        self.edit_dialog = None

    def set_controller(self, controller):
        self.controller = controller

    def build(self):
        self.page.title = "Gerenciador de Finanças"

        self.pages = [
            self.build_add_transaction_page(),
            self.build_transaction_list_page(),
            self.build_balance_page(),
        ]

        self.nav_buttons = ft.Row(
            [
                ft.ElevatedButton(text="Adicionar Transação", on_click=lambda e: self.show_page(0)),
                ft.ElevatedButton(text="Transações", on_click=lambda e: self.show_page(1)),
                ft.ElevatedButton(text="Balanço", on_click=lambda e: self.show_page(2)),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        self.page.controls.append(self.pages[0])
        self.page.controls.append(self.nav_buttons)
        self.page.update()

    def show_page(self, index):
        self.page.controls.pop(0)
        self.page.controls.insert(0, self.pages[index])
        self.page.update()

    def build_add_transaction_page(self):
        page_title = ft.Container(
            content=ft.Text('Gerenciador de Finanças', weight=ft.FontWeight.BOLD, size=42),
            padding=ft.Padding(top=10, bottom=20, left=0, right=0)
        )

        self.title_input = ft.TextField(label="Título")
        self.amount_input = ft.TextField(label="Quantia", keyboard_type=ft.KeyboardType.NUMBER)
        self.is_expense_checkbox = ft.Checkbox(label="É uma despesa")
        self.add_button = ft.ElevatedButton(text="Adicionar", on_click=self.add_transaction)
        column = ft.Column([page_title, self.title_input, self.amount_input, self.is_expense_checkbox, self.add_button], spacing=45, alignment=ft.MainAxisAlignment.CENTER,)
        return ft.Container(
            content=column,
            padding=ft.Padding(top=0, bottom=150, left=100, right=100)
        )
    
    def build_transaction_list_page(self):
        self.transaction_list = ft.ListView(height=500, spacing=10, padding=10)
        self.refresh_transactions()
        return self.transaction_list

    def build_balance_page(self):
        self.balance_label = ft.Container(
            content=ft.Text('', size=24, weight=ft.FontWeight.BOLD),
            padding=ft.Padding(top=10, bottom=10, left=0, right=0)
        )
        
        self.expense_label = ft.Container(
            content=ft.Text('', size=20, weight=ft.FontWeight.NORMAL),
            padding=ft.Padding(top=5, bottom=5, left=0, right=0)
        )
        
        self.income_label = ft.Container(
            content=ft.Text('', size=20, weight=ft.FontWeight.NORMAL),
            padding=ft.Padding(top=5, bottom=5, left=0, right=0)
        )
        
        self.balance_message = ft.Container(
            content=ft.Text('', size=18, weight=ft.FontWeight.NORMAL, color=ft.colors.BLUE),
            padding=ft.Padding(top=10, bottom=10, left=0, right=0)
        )

        return ft.Container(
            content=ft.Column(
                [self.balance_label, self.expense_label, self.income_label, self.balance_message],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER
            ),
        )

    def add_transaction(self, e):
        title = self.title_input.value
        amount = float(self.amount_input.value)
        is_expense = self.is_expense_checkbox.value
        self.controller.add_transaction(title, amount, is_expense)
        self.title_input.value = ""
        self.amount_input.value = ""
        self.is_expense_checkbox.value = False
        self.page.update()

    def refresh_transactions(self):
        transactions = self.controller.get_transactions()
        self.transaction_list.controls.clear()
        for t in transactions:
            color = ft.colors.RED if t.is_expense else ft.colors.GREEN
            item = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.REMOVE_CIRCLE if t.is_expense else ft.icons.ADD_CIRCLE, color=color, size=30),
                        ft.Column([ft.Text(t.title, weight=ft.FontWeight.BOLD, size=16), ft.Text(f"R$ {t.amount:.2f}", color=color, size=14)], expand=True),
                        ft.Row(
                            [
                                ft.IconButton(icon=ft.icons.EDIT, icon_color=ft.colors.BLUE_GREY, tooltip="Editar", on_click=lambda e, t=t: self.controller.start_edit_transaction(t)),
                                ft.IconButton(icon=ft.icons.DELETE, icon_color=ft.colors.RED, tooltip="Excluir", on_click=lambda e, t=t: self.controller.delete_transaction(t.id)),
                            ]
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=10,
                border_radius=10,
                bgcolor=ft.colors.with_opacity(0.05, ft.colors.GREY),
            )
            self.transaction_list.controls.append(item)
        self.page.update()

    def update_balance_labels(self, balance_text, expense_text, income_text, balance_message):
        self.balance_label.content.value = balance_text
        self.expense_label.content.value = expense_text
        self.income_label.content.value = income_text
        self.balance_message.content.value = balance_message
        self.page.update()

    def show_message(self, message):
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message), open=True)
        self.page.update()

    def show_edit_dialog(self, transaction):
        self.edit_title_input = ft.TextField(label="Título", value=transaction.title)
        self.edit_amount_input = ft.TextField(label="Quantia", value=str(transaction.amount), keyboard_type=ft.KeyboardType.NUMBER)
        self.edit_is_expense_checkbox = ft.Checkbox(label="É uma despesa", value=transaction.is_expense)
        self.edit_button = ft.ElevatedButton(text="Salvar", on_click=lambda e: self.controller.save_edit_transaction(transaction.id))
        self.cancel_button = ft.ElevatedButton(text="Cancelar", on_click=self.cancel_edit)
        
        edit_column = ft.Column(
            [self.edit_title_input, self.edit_amount_input, self.edit_is_expense_checkbox, self.edit_button, self.cancel_button],
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER
        )
        
        self.overlay = ft.Container(
            content=ft.Column(
                [ft.Container(
                    content=edit_column,
                    padding=ft.Padding(top=20, bottom=20, left=20, right=20),
                    border_radius=10,
                )],
                alignment=ft.MainAxisAlignment.CENTER,
                expand=True 
            ),
        )
        
        self.page.controls.append(self.overlay)
        self.page.update()

    def cancel_edit(self, e):
        if self.overlay in self.page.controls:
            self.page.controls.remove(self.overlay)
        self.overlay = None
        self.page.update()

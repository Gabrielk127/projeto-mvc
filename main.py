
from view.main_view import MainView
from controller.finance_controller import FinanceController

def main(page):
    view = MainView(page)
    controller = FinanceController(view)
    view.build()

if __name__ == "__main__":
    import flet as ft
    ft.app(target=main)

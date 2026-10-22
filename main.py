import streamlit as st
from classes import Transaction, FinanceManager
from datetime import date

FILE_NAME = 'data.txt'

st.set_page_config(page_title='Finance Manager', page_icon='💰')


if 'manager' not in st.session_state:
    st.session_state.manager = FinanceManager()
    st.session_state.loaded = False

manager = st.session_state.manager


def Load_data():
    try:
        file = open(FILE_NAME, 'r')
    except FileNotFoundError:
        file = open(FILE_NAME, 'w')
        file.close()
        return

    for line in file:
        line = line.strip()

        if line == '':
            continue

        parts = line.split(',', 4)

        try:
            d, t_type, category, amount, description = parts
            manager.Add(Transaction(d, t_type, category, float(amount), description))
        except ValueError:
            st.warning(f'Skipping corrupted line: {line}')

    file.close()


def Save_data():
    file = open(FILE_NAME, 'w')

    for t in manager.transactions:
        file.write(t.To_line() + '\n')

    file.close()


def Add_transaction_menu(t_type):
    st.subheader(f'Add {t_type.capitalize()}')

    with st.form(f'add_{t_type}', clear_on_submit=True):
        category = st.text_input('Category')
        amount = st.number_input('Amount', min_value=0.0, step=100.0, format='%.2f')
        description = st.text_input('Description')
        submitted = st.form_submit_button(f'Add {t_type}')

    if not submitted:
        return

    category = category.strip().replace(',', ' ')

    if category == '':
        st.error('Category cannot be empty')
        return

    if amount <= 0:
        st.error('Amount must be greater than 0')
        return

    description = description.strip().replace(',', ' ')

    manager.Add(Transaction(str(date.today()), t_type, category, amount, description))
    Save_data()
    st.success(f'{t_type.capitalize()} added')


def View_all():
    if len(manager.transactions) == 0:
        st.info('No transactions yet')
        return

    rows = []
    for i, t in enumerate(manager.transactions, 1):
        rows.append({
            '#': i,
            'Date': t.date,
            'Type': t.type_,
            'Category': t.category,
            'Amount': t.amount,
            'Description': t.description,
        })

    st.dataframe(rows, hide_index=True, use_container_width=True)


def Show_summary():
    st.metric('Balance', f'{manager.Balance():,.2f}')

    Dict = manager.Totals_by_category()

    if len(Dict) == 0:
        st.info('No expenses yet')
        return

    st.subheader('Spending by category')
    st.bar_chart(Dict)

    for category, total in Dict.items():
        st.write(f'{category} = {total}')


def Delete_menu():
    View_all()

    if len(manager.transactions) == 0:
        return

    num = st.number_input('Enter number to delete', min_value=1, step=1, value=1)

    if st.button('Delete'):
        if manager.Delete(int(num) - 1):
            Save_data()
            st.toast('Deleted')
            st.rerun()
        else:
            st.error('Invalid number')


def Main():
    if not st.session_state.loaded:
        Load_data()
        st.session_state.loaded = True

    st.title('Finance Manager')

    choice = st.sidebar.radio(
        'Menu',
        ['Add Income', 'Add Expense', 'View All', 'Summary', 'Delete']
    )

    if choice == 'Add Income':
        Add_transaction_menu('income')
    elif choice == 'Add Expense':
        Add_transaction_menu('expense')
    elif choice == 'View All':
        View_all()
    elif choice == 'Summary':
        Show_summary()
    elif choice == 'Delete':
        Delete_menu()


Main()
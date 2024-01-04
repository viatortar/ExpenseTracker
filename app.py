import streamlit as st
from db import Database


# Function to add transaction
def add_transaction_page(db):
    st.header("Tambah Transaksi")
    type_choice = st.selectbox("Pilih tipe transaksi", ['income', 'expense'])
    amount = st.text_input("Input Jumlah:")
    description = st.text_input("Input Deskripsi:")
    if st.button("Tambah Transaksi"):
        Database.add_transaction(db, (type_choice, amount, description))
        st.success("Transaction added successfully!")

# Function to view transactions
def view_transactions_page(db):
    st.header("Riwayat Transaksi")
    st.write("")
    transactions = Database.read_database(db)
    st.write("")
    if transactions:
        st.write("Transaksi:")
        st.dataframe(transactions, width=800)
    else:
        st.warning("Belum ada transaksi.")

# Function to edit transaction
def edit_transaction_page(db):
    st.header("Edit Transaksi")
    st.write("")
    transaction_id = st.text_input("Masukan Daftar ID transaksi yang ingin diedit")
    amount = st.text_input("Edit Jumlah")
    description = st.text_input("Edit Deskripsi")
    st.write("")
    if st.button("Edit"):
        Database.edit_transaction(db, (amount, description, transaction_id))
        st.success("Transaction edited successfully!")

# Function to delete transaction
def delete_transaction_page(db):
    st.header("Hapus Transaksi")
    st.write("")
    transaction_id = st.text_input("Masukan Daftar ID transaksi yang ingin dihapus")
    st.write("")
    if st.button("Hapus"):
        Database.delete_transaction(db, transaction_id)
        st.success("Transaction deleted successfully!")

# Function to show total balance
def total_balance_page(db):
    st.header("Total Saldo")
    st.write("")
    balance = Database.total_balance(db)
    st.write("Saldo Saat Ini:")
    st.info(f'Rp {int(balance):,.0f}')

# Main function
def main():
    db = Database.connect_to_database()

    # Hide the chain link in Streamlit
    hide_streamlit_style = """
            <style>
                #MainMenu {visibility: hidden;}
                .stDeployButton {display:none;}
                footer {visibility: hidden;}
                .css-15zrgzn {display: none}
                .css-eczf16 {display: none}
                .css-jn99sy {display: none}
            </style>
            """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Provide a unique key for the sidebar radio
    choice = st.sidebar.radio("Pilih Menu", ['Tambah Transaksi', 'Riwayat Transaksi', 'Edit Transaksi', 'Hapus Transaksi', 'Total Saldo'], key="unique_key")

    if choice == 'Tambah Transaksi':
        add_transaction_page(db)
    elif choice == 'Riwayat Transaksi':
        view_transactions_page(db)
    elif choice == 'Edit Transaksi':
        edit_transaction_page(db)
    elif choice == 'Hapus Transaksi':
        delete_transaction_page(db)
    elif choice == 'Total Saldo':
        total_balance_page(db)

    # Don't forget to close the connection when done
    db.close()

if __name__ == "__main__":
    main()

import db
from werkzeug.security import generate_password_hash, check_password_hash
import my_auth

def main():
    user = db.get_user("user@email.com")
    transactions = db.get_transactions_of_user(user)

    user2 = db.get_user("user2")
    transactions2 = db.get_transactions_of_user(user2)

    print('-' * 50)
    [print(transaction['title']) for transaction in transactions]
    print('-' * 50)
    [print(transaction['title']) for transaction in transactions2]
    print('-' * 50)
    print('-' * 50)

    categories = db.get_categories_of_user(user)
    [print(category['name']) for category in categories]


    # print_schema()

# Returns boolean depending on whether the transaction was able to be added to the db
def add_transaction(user, title:str, description:str, category_name:str, amount:float, recurring:bool, expense:bool) -> bool:
    flag = None
    category_id = get_category_id_by_name(user, category_name)
    if(category_id is None):
        print("Invalid category name")
        flag = False
        return flag
    try:
        db.create_transaction(user, title, description, category_id, amount, recurring, expense)
        flag = True
    except:
        flag = False
    return flag

def add_category(user, category_name:str) -> bool:
    flag = None
    try:
        db.create_category(user, category_name)
        flag = True
    except:
        flag = False
    return flag

# Returns the id of a category (int), or None if the category_name is invalid
def get_category_id_by_name(user, category_name:str):
    ret = None
    try:
        ret = db.get_category_id_by_name(user, category_name)
    except:
        ret = None
    return ret

if __name__ == "__main__":
    # main()
    flag = input("Create user? y/n")
    if flag.lower() == "y":
        username = input("Username")
        email = input("Email")
        password = input("Pass")

        print(my_auth.create_user(username, email, password))

    identifier = input("ID")
    password = input("Password")

    user = my_auth.login_user_from_form(identifier, password)
    if(user):
        print(user['id'])
    else:
        print("Failed login")
        exit()

    print("add category? y/n")
    flag = input()
    if(flag == "y"):
        in_name = input("Category name")
        if(add_category(user, in_name)):
            print("Category added successfully")
        else:
            print("Failed to add category")

    print("Add transaction? y/n")
    flag = input()
    if(flag == "y"):
        category_name:str = input("category_name")
        title:str = input("title")
        description:str = input("desc")
        amount:float = float(input("amount"))
        recurring_flag:bool = input("recurring?").lower() == "y"
        expense_flag:bool = input("expense?").lower() == "y"

        if(add_transaction(user, title, description, category_name, amount, recurring_flag, expense_flag)):
            print("transaction added successfully")
        else:
            print("Failed to add transaction")
    # print(db.get_transactions_of_user(user))
    [print(f"Title: {x['title']} | Description: {x['description']}") for x in db.get_transactions_of_user(user)]
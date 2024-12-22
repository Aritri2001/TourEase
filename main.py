import mysql.connector
import csv 


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "root1234",
    database = "travels"
)

cursor = db.cursor()


def add_customer():
    name = input("Enter name: ")
    phone = input("Enter phone number: ")  
    email = input("Enter email: ")
    city = input("Enter city: ")
    state = input("Enter state: ")
    food_pref = input("Enter food preference (veg/non-veg): ")

    try:
        query = "insert into customer (name, phone, email, city, state, food_pref) values (%s, %s, %s, %s, %s, %s)"
        values = (name, phone, email, city, state, food_pref)
        cursor.execute(query, values)
        db.commit()
        print("User added successfully!")
    except Exception as e:
        print(f"Error adding user: {e}")

def add_package():
    package_name = input("Enter package name: ")
    destination = input("Enter destination: ")
    description = input("Enter description: ")
    price = float(input("Enter price: "))
    duration = input("Enter duration: ")

    try:
        query = "insert into tour_package (package_name, destination, description, price, duration) values (%s, %s, %s, %s, %s)"
        values = (package_name, destination, description, price, duration)
        cursor.execute(query, values)
        db.commit()
        print("Package added successfully!")
    except Exception as e:
        print(f"Error adding package: {e}")

def make_booking():
    customer_id = int(input("Enter customer ID: "))
    package_id = int(input("Enter package ID: "))
    number_of_people = int(input("Enter number of people: "))

    try:
        query = "insert into booking (customer_id, package_id, people) values (%s, %s, %s)"
        values = (customer_id, package_id, number_of_people)
        cursor.execute(query, values)
        db.commit()
        print("Booking made successfully!")
        booking_id = cursor.lastrowid
        price_query = "select price from tour_package where package_id = %s"
        cursor.execute(price_query, (package_id,))  
        package_price = cursor.fetchone()[0]  
        total_payment = number_of_people * package_price
        print("Initiating payment...")
        do_payment(booking_id, total_payment)

    except Exception as e:
        print(f"Error making booking: {e}")

def do_payment(booking_id, amount):
    print(f"Payable amount : {amount}")
    while True:
        payment_method = input("Enter payment method (credit_card/debit_card/UPI/cash): ").lower()
        if payment_method == "credit_card":
            amount = amount * 0.85
            print(f"15% discount applied! amount paid: {amount}")

        try:
            query = "insert into payment (booking_id, amount, method) values (%s, %s, %s)"
            values = (booking_id, amount, payment_method)
            cursor.execute(query, values)
            db.commit()
            print("Payment recorded successfully!")
            break
        except Exception as e:
            print(f"Error doing payment: {e}")

def view_data(table_name):
    try:
        query = f"show columns from {table_name}"
        cursor.execute(query)
        headers = [column[0] for column in cursor.fetchall()]
        print(headers)

        query = f"select * from {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Exception as e:
        print(f"Error fetching data: {e}")

def delete_record(table_name,id):
        record_id = input(f"Enter the ID of the record to delete from {table_name}: ")
        try:
            query = f"delete from {table_name} where {id} = %s"
            cursor.execute(query, (record_id,))
            db.commit()

            if cursor.rowcount > 0:
                print(f"Record with ID {record_id} deleted successfully from {table_name}.")
            else:
                print(f"No record found with ID {record_id} in {table_name}.")
        except Exception as e:
            print(f"Error deleting record: {e}")

def search_table(table_name):
    try:
        query = f"show columns from {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
        headers = [column[0] for column in results]

        if results:
            print(f"Available columns in {table_name}:")
            for column in results:
                print(column[0])  

        column_name = input("Enter the column name to search: ").strip()
        search_value = input("Enter the value to search for: ").strip()

        valid_columns = [column[0] for column in results]
        if column_name not in valid_columns:
            print(f"Invalid column name. Please choose from: {', '.join(valid_columns)}")
            return

        query = f"select * from {table_name} where {column_name} like %s"
        cursor.execute(query, (f"%{search_value}%",))
        search_results = cursor.fetchall()

        if search_results:
            print(f"\nSearch results for '{search_value}' in column '{column_name}':")
            print(headers)
            for row in search_results:
                print(row)
        else:
            print(f"No results found for {column_name} containing '{search_value}' in {table_name}.")

    except Exception as e:
        print(f"Error searching the table: {e}")

def export_to_csv(table_name,file_name):
        filename = f"{file_name}.csv"
        try:
            cursor.execute(f"select * from {table_name}")
            results = cursor.fetchall()
            headers = [desc[0] for desc in cursor.description]

            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(headers)  
                writer.writerows(results)  

            print(f"Data from {table_name} table successfully exported to {filename}")
        except Exception as e:
            print(f"Error exporting data: {e}")



def main():
    print("Welcome to the TourEase platform")

    while True:
        print("1. Customer")
        print("2. Package")
        print("3. Booking")
        print("4. Payment")
        print("5. Export data")
        print("6. Exit")

        choice = int(input("Enter your choice:"))
        if choice == 1:
            print("1. Add Customer")
            print("2. View Customer")
            print("3. Search Customer")
            print("4. Remove Customer")
            print("5. Go to Home")
            sub_choice = int(input("Enter your choice:"))
            if sub_choice == 1:
                add_customer()
            elif sub_choice == 2:
                view_data("customer")
            elif sub_choice == 3:
                search_table("customer")   
            elif sub_choice == 4:
                delete_record("customer","customer_id")
            else :
                main()

        elif choice == 2:
            print("1. Add Package")
            print("2. View Package")
            print("3. Search Package")
            print("4. Remove Package")
            print("5. Go to Home")
            sub_choice = int(input("Enter your choice:"))
            if sub_choice == 1:
                add_package()
            elif sub_choice == 2:
                view_data("tour_package")
            elif sub_choice == 3:
                search_table("tour_package")
            elif sub_choice == 4:
                delete_record("tour_package","package_id")
            else :
                main()

        elif choice == 3:
            print("1. Make Booking")
            print("2. View Booking")
            print("3. Search Booking")       
            print("4. Remove Booking")
            print("5. Go to Home")
            sub_choice = int(input("Enter your choice:"))
            if sub_choice == 1:
                make_booking()
            elif sub_choice == 2:
                view_data("booking")
            elif sub_choice == 3:
                search_table("booking")
            elif sub_choice == 4:
                delete_record("booking","booking_id")
            else :
                main()

        elif choice == 4:
            print("1. View Payments")
            print("2. Search Payments")
            print("3. Remove Payments")
            print("4. Go to Home")
            sub_choice = int(input("Enter your choice:"))
            if sub_choice == 1:
                view_data("payment")
            elif sub_choice == 2:
                search_table("payment")
            elif sub_choice == 3:
                delete_record("payment","payment_id")
            else :
                main()


        elif choice == 5:
            print("1. Export Customers Data")
            print("2. Export Packages Data")
            print("3. Export Bookings Data")
            print("4. Export Payments Data")
            print("5. Go to Home")
            sub_choice = int(input("Enter your choice:"))
            if sub_choice == 1:
                export_to_csv("customer","Customers")
            elif sub_choice == 2:
                export_to_csv("tour_package","Packages")
            elif sub_choice == 3:
                export_to_csv("booking","Bookings")
            elif sub_choice == 4:
                export_to_csv("payment","Payments")
            else :
                main()

        elif choice == 6:
            print("Thank you for using TourEase platform")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()


cursor.close()
db.close()
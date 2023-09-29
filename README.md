# BookStore: Your Online Literary Haven 📚

Welcome to BookStore, your one-stop destination for exploring, purchasing, and sharing the world of books. Whether you're an avid reader, an aspiring author, or simply a book enthusiast, this Django-powered online bookstore has something for everyone.

## Features

🔒 **User Authentication**:
Users are able to register, log in, and log out.
Only logged-in users can view and manage their cart.

📖 **Book Management**:
Implements functionality to add, edit, and delete books.
Each book has a title, author, genre, price, and available quantity.

🔍 **View Books**:
Displays a list of available books to users.
Provides options for users to filter and search for books by title, author, or genre.

🛒 **Shopping Cart**:
Users are able to add books to their cart and specify the quantity.
Displays the contents of the cart and allow users to modify or remove items from the cart.

💳 **Checkout and Order History**:
Allows users to proceed to checkout, providing a summary of the order.

📚 **Book Details**:
When a user clicks on a book, displays detailed information about the book.

💻 **User Interface**:
A clean and intuitive user interface for the application.
Uses HTML/CSS to create a responsive design.

## Installation

Follow these steps to set up BookStore on your local machine:

1. Clone this repository:
git clone https://github.com/ranjodh55/final-project.git


2. Navigate to the project directory:
cd final-project


3. Create a virtual environment and activate it:
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate


4. Install the project dependencies:
pip install -r requirements.txt


5. Run database migrations:
python manage.py migrate


6. Create a superuser account:
python manage.py createsuperuser

7. Add your email and password in project/settings.py file for the sending email functionality to work. You don't have to add your actual password there instaed add app password. You can get it from accounts.google.com > search 'App passwords' > create a new one. Make sure to remove all spaces from the password while pasting it in settings.py. It should be like this
EMAIL_HOST_USER = 'your_email'
EMAIL_HOST_PASSWORD = 'your_app_password'
   

9. Start the development server:
python manage.py runserver

10. Access the application in your web browser.

## Technologies Used

- Django: Web framework
- HTML/CSS: Front-end design
- MySql: Database
<br><br>
# ***** Overview of the project *****<br><br># Homepage : 
![book_home_page](https://github.com/ranjodh55/final-project/assets/59740585/7800cb97-af0a-484d-aed7-4ef757c3779b)

![book_home_page2](https://github.com/ranjodh55/final-project/assets/59740585/1eab5052-99ac-4d6c-a6e7-0140777e8b25)

![book_home_page3](https://github.com/ranjodh55/final-project/assets/59740585/66013ada-4929-45f4-a2c1-2166e498d464)

# Genre-wise Book listing
![book_genre](https://github.com/ranjodh55/final-project/assets/59740585/3dec9bc2-877c-4da3-b94b-c92f1dc63b91)

# Sort : Ascending
![book_sort_up](https://github.com/ranjodh55/final-project/assets/59740585/1437382d-3cd6-4396-9806-b1920855c28f)

# Sort : Descending
![book_dort_down](https://github.com/ranjodh55/final-project/assets/59740585/34091cc5-6316-44b8-ab24-87c494d66fce)

# Search Books
![book_search](https://github.com/ranjodh55/final-project/assets/59740585/05a82103-2b61-45ed-afdc-d4403694fa1f)

# Book Details
![book_detail](https://github.com/ranjodh55/final-project/assets/59740585/a16dbebf-bfdd-4033-aa3e-b4abd74ba90d)

# Cannot add quantity more than available quantity
![book_exceed_quan](https://github.com/ranjodh55/final-project/assets/59740585/b41627bc-9e7c-457d-bd04-bf9459b6a602)

# Cart
![book_cart](https://github.com/ranjodh55/final-project/assets/59740585/a9ced853-0357-4944-8e8f-37af4d7beb82)

# Order placed
![book_order_placed](https://github.com/ranjodh55/final-project/assets/59740585/0a0d144e-de6d-489c-907b-ee88342010be)

# Login
![book_sign_in](https://github.com/ranjodh55/final-project/assets/59740585/39d6f5b4-963c-4938-b207-93fdf4d95faa)

# Sign Up
![book_sign_up](https://github.com/ranjodh55/final-project/assets/59740585/c08cb85b-5ab6-41a0-9eab-242d8bf5fb1b)

# Email verification on registration
![Screenshot from 2023-09-29 14-21-50](https://github.com/ranjodh55/final-project/assets/59740585/a7dac76f-4f13-44b2-b3bf-c04cd6b8ac4e)

![Screenshot from 2023-09-29 14-22-20](https://github.com/ranjodh55/final-project/assets/59740585/88ca89aa-0678-4397-bddd-8fb61c45edf8)


# Forgot Password
![Screenshot from 2023-09-29 14-23-22](https://github.com/ranjodh55/final-project/assets/59740585/46d42f72-6b05-4c31-9c6c-6bb6e1142a25)


# Admin
![Screenshot from 2023-09-29 14-25-57](https://github.com/ranjodh55/final-project/assets/59740585/c6723047-e809-4344-b548-f51b284af244)

# Searching sorting Admin panel
![Screenshot from 2023-09-29 14-26-04](https://github.com/ranjodh55/final-project/assets/59740585/c8dd3ec8-edbf-4148-84f9-31658cf23d0a)


# Encrypted User password
![Screenshot from 2023-09-29 14-26-38](https://github.com/ranjodh55/final-project/assets/59740585/a4f53522-b0a7-45d5-b324-cba51ede348d)

Happy reading! 📖















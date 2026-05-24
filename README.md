# MediWay

MediWay is a Django-based online pharmacy and medical store management system. It allows users to browse medicines, search the medicine catalog, add items to a cart, upload prescriptions when required, complete payment through Razorpay, track orders, and download invoices. The admin side supports medicine management, bulk medicine upload, order status updates, billing, and invoice generation.

## Table of Contents

1. Introduction
2. Key Features
3. Project Objectives
4. Technology Stack
5. Project Folder Structure
6. User Workflow
7. Module-Wise Documentation
8. Admin Workflow
9. Database Design
10. Testing
11. Conclusion
12. Future Scope
13. Screenshot Order
14. Code Presentation Order
15. Formatting Guidelines

## 1. Introduction

MediWay is an online pharmacy and medical store management system designed to simplify medicine ordering and pharmacy administration. Users can browse medicines, search for products, upload prescriptions for restricted medicines, place orders, make secure payments, view order history, and download invoices.

The admin can manage medicine records, upload medicines in bulk, view customer orders, update order status, and generate bills. This reduces manual pharmacy work and maintains organized digital records for orders, medicines, prescriptions, and invoices.

**Add Screenshot Here:** Homepage / Medicine Catalog screenshot

**Caption:** Figure 5.1: MediWay Home Page

## 2. Key Features

- User authentication with signup, login, logout, and profile update
- Medicine catalog with search functionality
- Fuzzy medicine search using `fuzzywuzzy`
- Shopping cart with quantity update and item removal
- Prescription upload for medicines that require prescriptions
- Razorpay payment gateway integration
- Order confirmation and order history
- Billing and invoice PDF generation
- Admin dashboard for medicine management
- Bulk medicine upload using CSV or Excel files
- Admin order management and status tracking

**Add Screenshots Here:**

- Search bar screenshot
- Cart page screenshot
- Invoice page screenshot
- Admin dashboard screenshot

## 3. Project Objectives

- Simplify online medicine ordering for customers
- Reduce manual pharmacy management work
- Enable secure online payments
- Maintain digital order and billing records
- Generate invoices automatically
- Support prescription-based medicine purchases
- Help admins manage medicine inventory efficiently

## 4. Technology Stack

| Technology | Purpose |
| --- | --- |
| Python | Backend logic |
| Django | Web framework |
| SQLite | Database |
| HTML/CSS | Frontend pages and styling |
| Razorpay | Payment gateway |
| pandas | Bulk medicine upload |
| xhtml2pdf | Invoice PDF generation |
| fuzzywuzzy | Fuzzy medicine search |

## 5. Project Folder Structure

**Add Screenshot Here:** VS Code project structure screenshot

```text
MediWay/
|
|-- core/
|-- mediway/
|-- templates/
|-- static/
|-- media/
|-- prescriptions/
|-- manage.py
|-- db.sqlite3
`-- requirements.txt
```

### Folder Purpose

`core/`

Contains the main Django application files such as `models.py`, `views.py`, `urls.py`, `forms.py`, and `admin.py`.

`mediway/`

Contains Django project configuration files such as `settings.py`, root `urls.py`, `wsgi.py`, and `asgi.py`.

`templates/`

Contains all HTML pages including login, signup, home, cart, orders, billing, invoice, dashboard, and admin order pages.

`static/`

Contains static frontend assets such as images, CSS, JavaScript, and logo files.

`media/` and `prescriptions/`

Stores uploaded files such as prescription documents.

`manage.py`

Django command-line utility used to run the server, migrations, and administrative commands.

`db.sqlite3`

SQLite database file used for local development.

## 6. User Workflow

### A. User Workflow Flowchart

```text
Home Page
    |
Signup
    |
Login
    |
Browse Medicines
    |
Search Medicines
    |
Add to Cart
    |
Upload Prescription (if required)
    |
Checkout
    |
Razorpay Payment
    |
Order Confirmation
    |
Order History
    |
Invoice Download
    |
Logout
```

## 7. Module-Wise Documentation

### Module 1: User Authentication

**Add Screenshots Here:**

- Signup page
- Login page
- Profile page
- Logout redirect page

**Screenshot Captions:**

- Figure 11.1: User Signup Page
- Figure 11.2: User Login Page
- Figure 11.3: User Profile Management

**Code Sequence:**

1. `templates/signup.html`
2. `templates/login.html`
3. `templates/profile.html`
4. `core/views.py` -> `signup_view()`
5. `core/views.py` -> `login_view()`
6. `core/views.py` -> `logout_view()`
7. `core/views.py` -> `profile_view()`
8. `core/urls.py`

**Explanation:**

The authentication module allows users to create an account, log in using email and password, update profile details, and log out securely. Django's built-in `User` model is used for storing user credentials. The session is created after successful login and destroyed during logout.

### Module 2: Medicine Catalog

**Add Screenshots Here:**

- Homepage medicine listing
- Search functionality
- Search results page

**Screenshot Captions:**

- Figure 12.1: Medicine Catalog
- Figure 12.2: Medicine Search System

**Code Sequence:**

1. `templates/home.html`
2. `templates/medicine_detail.html`
3. `core/models.py` -> `Medicine`
4. `core/views.py` -> `home()`
5. `core/views.py` -> `medicine_detail()`
6. `core/urls.py`
7. `core/admin.py`

**Explanation:**

The medicine catalog displays available medicines from the database. Users can search medicines by name or company. The search system also uses `fuzzywuzzy` to find close matches when the user enters an approximate medicine name. Pagination is used to show medicines in a clean and manageable format.

### Module 3: Cart Management

**Flow:**

```text
Select Medicine
    |
Add to Cart
    |
Update Quantity
    |
Remove Item
    |
Proceed to Checkout
```

**Add Screenshots Here:**

- Cart page
- Quantity update
- Remove item
- Checkout page

**Code Sequence:**

1. `templates/cart.html`
2. `core/models.py` -> `Cart`
3. `core/views.py` -> `add_to_cart()`
4. `core/views.py` -> `cart_view()`
5. `core/views.py` -> `update_cart()`
6. `core/views.py` -> `remove_from_cart()`
7. `core/views.py` -> `checkout()`
8. `core/urls.py`

**Explanation:**

The cart module stores selected medicines for each logged-in user. Users can increase or decrease medicine quantity, remove medicines, and proceed to checkout. The system calculates item totals and the grand total before payment.

### Module 4: Prescription Upload

**Add Screenshots Here:**

- Prescription upload form
- Uploaded prescription preview

**Code Sequence:**

1. `templates/upload_prescriptions.html`
2. `core/models.py` -> `Cart.prescription_file`
3. `core/models.py` -> `Order.prescription_file`
4. `core/views.py` -> `upload_prescriptions()`
5. `core/urls.py`

**Explanation:**

Some medicines require a valid prescription. When the cart contains prescription-required medicines, the user is redirected to the prescription upload page before payment. Uploaded files are stored in the prescriptions upload directory and later linked with the order record.

### Module 5: Razorpay Payment Integration

**Workflow:**

```text
Checkout
    |
Razorpay Gateway
    |
Payment Success
    |
Order Created
```

**Add Screenshots Here:**

- Payment page
- Razorpay popup
- Payment success page

**Code Sequence:**

1. `templates/payment.html`
2. `templates/success.html`
3. `templates/failed.html`
4. `core/views.py` -> `create_payment()`
5. `core/views.py` -> `verify_payment()`
6. `core/views.py` -> `payment_success()`
7. `mediway/settings.py` -> Razorpay keys
8. `core/urls.py`

**Explanation:**

The payment module creates a Razorpay order for the cart total. After payment, payment details are verified and the order status is updated. Successful payments create order records and clear the user's cart.

### Module 6: Order Management

**Add Screenshots Here:**

- Order history page
- Order details page
- Order status tracking

**Code Sequence:**

1. `templates/orders.html`
2. `templates/order_detail.html`
3. `core/models.py` -> `Order`
4. `core/views.py` -> `orders_view()`
5. `core/views.py` -> `order_detail()`
6. `core/urls.py`

**Explanation:**

The order management module allows users to view all previous orders and inspect details such as medicine name, quantity, total amount, prescription file, payment status, and order status. Admin users can update order status from the admin order pages.

### Module 7: Billing & Invoice System

**Add Screenshots Here:**

- Billing form
- Invoice page
- PDF download

**Code Sequence:**

1. `templates/billing.html`
2. `templates/invoice.html`
3. `templates/invoice_pdf.html`
4. `core/models.py` -> `Bill`
5. `core/models.py` -> `BillItem`
6. `core/views.py` -> `billing()`
7. `core/views.py` -> `set_customer()`
8. `core/views.py` -> `add_to_bill()`
9. `core/views.py` -> `generate_bill()`
10. `core/views.py` -> `generate_pdf()`
11. `core/views.py` -> `download_invoice()`
12. `core/urls.py`

**Explanation:**

The billing module stores customer details and selected medicines for billing. After bill generation, bill items are saved in the database and the invoice page is displayed. The project uses `xhtml2pdf` to convert invoice HTML into a downloadable PDF.

## 8. Admin Workflow

### Admin Flowchart

```text
Admin Login
    |
Dashboard
    |
Add Medicines
    |
Edit Medicines
    |
Delete Medicines
    |
Bulk Upload Medicines
    |
Manage Orders
    |
Update Order Status
    |
Billing Management
    |
Logout
```

### Module 8: Admin Dashboard

**Add Screenshots Here:**

- Admin dashboard
- Add medicine page
- Edit medicine page
- Delete confirmation
- Bulk upload page
- Admin order management page

**Code Sequence:**

1. `templates/dashboard.html`
2. `templates/edit_medicine.html`
3. `templates/upload_bulk.html`
4. `templates/admin_orders.html`
5. `templates/admin_order_detail.html`
6. `core/models.py` -> `Medicine`, `Order`
7. `core/admin.py`
8. `core/views.py` -> `dashboard()`
9. `core/views.py` -> `add_medicine()`
10. `core/views.py` -> `edit_medicine()`
11. `core/views.py` -> `delete_medicine()`
12. `core/views.py` -> `upload_medicines_csv()`
13. `core/views.py` -> `admin_orders()`
14. `core/views.py` -> `admin_order_detail()`
15. `core/views.py` -> `update_order_status()`
16. `core/urls.py`

**Explanation:**

The admin dashboard is available only to superusers. It allows the admin to add, edit, and delete medicine records. Admins can upload medicine data in bulk through CSV or Excel files. The order management section allows admins to view customer orders and update statuses such as pending, approved, rejected, shipped, and delivered.

## 9. Database Design

**Add Screenshot Here:** Database tables screenshot from SQLite Browser

### Main Tables

| Table | Purpose |
| --- | --- |
| `auth_user` | Stores user account information |
| `core_medicine` | Stores medicine details |
| `core_cart` | Stores user cart items |
| `core_order` | Stores order and payment information |
| `core_bill` | Stores customer bill records |
| `core_billitem` | Stores individual bill medicine items |

### Table Explanation

`User`

Stores username, email, password, and account details using Django's built-in authentication system.

`Medicine`

Stores medicine name, price, company, size, image path, prescription requirement, and safety warning.

`Cart`

Stores medicines temporarily selected by a user before checkout.

`Order`

Stores confirmed medicine orders, prescription file, payment details, order status, and timestamps.

`Bill`

Stores customer billing details such as name, mobile number, email, total amount, and bill creation date.

`BillItem`

Stores medicines included in a bill along with quantity and price.

## 10. Testing

**Add Screenshots Here:**

- Successful login
- Invalid login
- Empty cart validation
- Prescription upload validation
- Payment success
- Order history display
- Invoice generation
- Admin status update

### Suggested Test Cases

| Test Case | Expected Result |
| --- | --- |
| Valid user login | User redirects to home page |
| Invalid user login | Error message is displayed |
| Add medicine to cart | Medicine appears in cart |
| Update cart quantity | Cart total changes correctly |
| Checkout with empty cart | User remains on cart page |
| Checkout with prescription medicine | User is redirected to prescription upload |
| Successful payment | Order is created and cart is cleared |
| Generate invoice | Invoice page and PDF download are available |
| Admin updates order status | New order status is saved |

## 11. Conclusion

MediWay successfully automates important pharmacy management activities such as medicine browsing, prescription upload, online payment, order tracking, billing, and invoice generation. The system improves customer convenience and reduces manual work for pharmacy admins by maintaining organized digital records.

## 12. Future Scope

- AI-based medicine recommendation
- Online doctor consultation
- Email and SMS notifications
- Inventory analytics
- Cloud deployment
- Stock alert system
- Advanced prescription verification
- Online refund and cancellation support

## 13. Screenshot Order

Use this screenshot order in the final project report:

1. Home
2. Signup
3. Login
4. Medicine Catalog
5. Search
6. Cart
7. Prescription Upload
8. Checkout
9. Payment
10. Order Success
11. Order History
12. Invoice
13. Profile
14. Logout
15. Admin Login
16. Admin Dashboard
17. Add/Edit/Delete Medicine
18. Bulk Upload
19. Order Management

## 14. Code Presentation Order

For every module, present the code in this order:

1. HTML Template
2. `forms.py`
3. `models.py`
4. `views.py`
5. `urls.py`
6. `admin.py`

This order looks professional and helps examiners understand the frontend, data layer, logic, routing, and admin configuration step by step.

## 15. Formatting Guidelines

Use these formatting rules in the final Word/PDF report:

| Element | Formatting |
| --- | --- |
| Heading 1 | 18 pt, Bold |
| Heading 2 | 16 pt, Bold |
| Heading 3 | 14 pt, Bold |
| Normal text | Times New Roman, 12 pt |
| Code | Consolas font, light gray background |
| Screenshots | Thin black border |
| Captions | Below each image |

## Setup

1. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Apply migrations.

```bash
python manage.py migrate
```

4. Create an admin user.

```bash
python manage.py createsuperuser
```

5. Run the development server.

```bash
python manage.py runserver
```

6. Open the application.

```text
http://127.0.0.1:8000/
```

## Common Routes

| Route | Purpose |
| --- | --- |
| `/` | Medicine catalog |
| `/signup/` | User signup |
| `/login/` | User login |
| `/logout/` | User logout |
| `/profile/` | User profile |
| `/cart/` | Shopping cart |
| `/checkout/` | Checkout flow |
| `/upload-prescriptions/` | Prescription upload |
| `/payment/` | Razorpay payment |
| `/orders/` | User order history |
| `/dashboard/` | Admin medicine dashboard |
| `/admin-orders/` | Admin order management |
| `/billing/` | Billing workflow |
| `/invoice/<id>/` | Invoice view |
| `/download-invoice/<id>/` | PDF invoice download |
| `/admin/` | Django admin panel |

# Banking App

A full-featured banking application built with Flask and SQLite that allows users to manage their bank accounts with deposit, withdrawal, balance checking, and interest calculation features.

## Features

✅ **User Authentication** - Secure registration and login with password hashing
✅ **Multiple Accounts** - Create and manage multiple bank accounts per user
✅ **Deposit Money** - Add funds to your account
✅ **Withdraw Money** - Remove funds from your account (with balance validation)
✅ **Check Balance** - View current account balance at any time
✅ **Transaction History** - Complete record of all transactions with timestamps
✅ **Interest Calculation** - Automatic 5% annual interest (monthly compounding)
✅ **Responsive Design** - Works on desktop and mobile devices
✅ **Beautiful UI** - Modern, gradient-based design with smooth interactions


## How this was built

I built this project with [Claude](https://claude.ai) as an AI coding assistant. My role was directing the work: I decided what the project should do, broke it into features, and wrote the prompts that guided Claude through building each one. Claude wrote the code.

## Tech Stack

- **Backend**: Flask 2.3.3 (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Authentication**: Flask-Login with password hashing

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/rkaraca2029/Banking-Web-App.git
cd Banking-Web-App
```

### 2. Create a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Running the Application

### 1. Activate the virtual environment
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Run the Flask app
```bash
python run.py
```

The application will start on `http://localhost:5001`

### 3. Open in your browser
Navigate to `http://localhost:5001` in your web browser.

## Usage

### Creating an Account
1. Click "Register here" on the login page
2. Enter username, email, and password
3. A default checking account will be created automatically
4. Login with your credentials

### Managing Your Account
1. **View Accounts**: See all your accounts on the dashboard
2. **Deposit**: Click "View Details" and enter the amount to deposit
3. **Withdraw**: Enter the withdrawal amount (must be ≤ current balance)
4. **Apply Interest**: Receive monthly interest (5% annual rate)
5. **View History**: See complete transaction history with timestamps

## Project Structure

```
Banking-Web-App/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── models.py             # Database models (User, Account, Transaction)
│   ├── routes.py             # API routes and views
│   ├── templates/
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   ├── dashboard.html    # Account dashboard
│   │   └── account_details.html  # Account details page
│   └── static/
│       └── css/
│           └── style.css     # Styling
├── config.py                 # Configuration settings
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Database Models

### User
- `id`: Primary key
- `username`: Unique username
- `password_hash`: Hashed password
- `email`: User email
- `created_at`: Account creation timestamp

### Account
- `id`: Primary key
- `user_id`: Foreign key to User
- `account_number`: Unique 16-digit account number
- `account_type`: Type of account (Checking, Savings)
- `balance`: Current account balance
- `created_at`: Account creation timestamp

### Transaction
- `id`: Primary key
- `account_id`: Foreign key to Account
- `transaction_type`: Type (deposit, withdraw, interest)
- `amount`: Transaction amount
- `balance_after`: Balance after transaction
- `description`: Transaction description
- `created_at`: Transaction timestamp

## API Endpoints

### Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `GET /logout` - Logout user

### Accounts
- `GET /api/accounts` - Get all user accounts
- `GET /api/account/<id>` - Get specific account

### Transactions
- `POST /api/account/<id>/deposit` - Deposit money
- `POST /api/account/<id>/withdraw` - Withdraw money
- `POST /api/account/<id>/apply-interest` - Apply monthly interest
- `GET /api/account/<id>/transactions` - Get transaction history

## Security Features

- **Password Hashing**: Uses Werkzeug's secure hashing
- **Session Management**: Flask-Login handles user sessions
- **Authorization Checks**: Ensures users can only access their own accounts
- **Input Validation**: All inputs are validated before processing

## Future Enhancements

- [ ] Two-factor authentication
- [ ] Transfer money between accounts
- [ ] Scheduled transfers
- [ ] Bill payment functionality
- [ ] Mobile app
- [ ] Email notifications
- [ ] Export transaction history to CSV
- [ ] Multiple currencies support

## Troubleshooting

**"Address already in use" error**
- Change the port number in `run.py` (the app uses 5001 by default)

**Database issues**
- Delete `instance/banking.db` and restart the app to reset the database

**Module not found**
- Ensure virtual environment is activated and all dependencies are installed

## License

This project is open source and available under the MIT License.

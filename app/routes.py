from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User, Account, Transaction
from datetime import datetime
import random
import string
from config import Config

main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ============ MAIN ROUTES ============

@main_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Create a default checking account
        account = Account(
            user_id=user.id,
            account_number=generate_account_number(),
            account_type='Checking',
            balance=0.0
        )
        db.session.add(account)
        db.session.commit()
        
        return jsonify({'message': 'Registration successful'}), 201
    
    return render_template('register.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200
        
        return jsonify({'error': 'Invalid username or password'}), 401
    
    return render_template('login.html')

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', accounts=accounts)

@main_bp.route('/account/<int:account_id>')
@login_required
def account_details(account_id):
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return redirect(url_for('main.dashboard'))
    
    transactions = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.created_at.desc()).all()
    return render_template('account_details.html', account=account, transactions=transactions)

# ============ API ROUTES ============

@api_bp.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    accounts = Account.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': a.id,
        'account_number': a.account_number,
        'account_type': a.account_type,
        'balance': a.balance,
        'created_at': a.created_at.strftime('%Y-%m-%d')
    } for a in accounts])

@api_bp.route('/account/<int:account_id>', methods=['GET'])
@login_required
def get_account(account_id):
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'id': account.id,
        'account_number': account.account_number,
        'account_type': account.account_type,
        'balance': account.balance,
        'created_at': account.created_at.strftime('%Y-%m-%d')
    })

@api_bp.route('/account/<int:account_id>/deposit', methods=['POST'])
@login_required
def deposit(account_id):
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    amount = data.get('amount', 0)
    
    if amount <= 0:
        return jsonify({'error': 'Deposit amount must be positive'}), 400
    
    account.balance += amount
    
    transaction = Transaction(
        account_id=account_id,
        transaction_type='deposit',
        amount=amount,
        balance_after=account.balance,
        description=f'Deposit of ${amount:.2f}'
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Deposit successful',
        'new_balance': account.balance,
        'transaction': {
            'type': transaction.transaction_type,
            'amount': transaction.amount,
            'balance_after': transaction.balance_after,
            'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@api_bp.route('/account/<int:account_id>/withdraw', methods=['POST'])
@login_required
def withdraw(account_id):
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    amount = data.get('amount', 0)
    
    if amount <= 0:
        return jsonify({'error': 'Withdrawal amount must be positive'}), 400
    
    if amount > account.balance:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    account.balance -= amount
    
    transaction = Transaction(
        account_id=account_id,
        transaction_type='withdraw',
        amount=amount,
        balance_after=account.balance,
        description=f'Withdrawal of ${amount:.2f}'
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Withdrawal successful',
        'new_balance': account.balance,
        'transaction': {
            'type': transaction.transaction_type,
            'amount': transaction.amount,
            'balance_after': transaction.balance_after,
            'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@api_bp.route('/account/<int:account_id>/transactions', methods=['GET'])
@login_required
def get_transactions(account_id):
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    transactions = Transaction.query.filter_by(account_id=account_id).order_by(Transaction.created_at.desc()).all()
    
    return jsonify([{
        'id': t.id,
        'type': t.transaction_type,
        'amount': t.amount,
        'balance_after': t.balance_after,
        'description': t.description,
        'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for t in transactions])

@api_bp.route('/account/<int:account_id>/apply-interest', methods=['POST'])
@login_required
def apply_interest(account_id):
    account = Account.query.get(account_id)
    
    if not account or account.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    interest_amount = account.balance * Config.INTEREST_RATE / 12  # Monthly interest
    account.balance += interest_amount
    
    transaction = Transaction(
        account_id=account_id,
        transaction_type='interest',
        amount=interest_amount,
        balance_after=account.balance,
        description='Monthly interest credit'
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({
        'message': 'Interest applied',
        'interest_amount': interest_amount,
        'new_balance': account.balance
    })

# ============ HELPER FUNCTIONS ============

def generate_account_number():
    """Generate a unique account number."""
    return ''.join(random.choices(string.digits, k=16))

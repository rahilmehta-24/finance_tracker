from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_wtf.csrf import CSRFProtect
import pandas as pd
import calendar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
csrf = CSRFProtect(app)

# Update this URI as per your PostgreSQL setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rahil123@localhost:5432/transaction'
db = SQLAlchemy(app)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, default=datetime.date.today)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def index():
    month = request.args.get('month')
    year = request.args.get('year')
    query = Transaction.query
    if month and year:
        start_date = datetime.date(int(year), int(month), 1)
        if int(month) == 12:
            end_date = datetime.date(int(year) + 1, 1, 1) - datetime.timedelta(days=1)
        else:
            end_date = datetime.date(int(year), int(month) + 1, 1) - datetime.timedelta(days=1)
        query = query.filter(Transaction.date.between(start_date, end_date))
    transactions = query.all()
    return render_template('index.html', transactions=transactions)

def get_categories():
    return [
        'Milk Exp', 'Vegetable Exp', 'Laundry Exp', 'DTH Exp', 'Broadband Exp',
        'Newspaper Exp', 'Electricity Exp', 'Adani Gas Exp', 'Mobile recharge exp',
        'Tuition Fee', 'Sports Fee', 'Medical Exp', 'Housekeeping', 'Car Ins Premium',
        'Car Service', 'Scooter Ins Premium', 'Scooter Service', 'Society Maintenance',
        'Grocery Exp', 'Mediclaim Premium', 'Entertainment Exp (Other OTT)',
        'Entertainment Exp (Netflix)', 'Miscellaneous Exp', 'Miscellaneous Exp (Food)',
        'Miscellaneous Exp (Travel)', 'Life Insurance Premium', 'Conveyance(Fuel) Exp',
        'Clothes Exp', 'Housing Loan EMI', 'Car Loan EMI', 'Appliances EMI', 'PPF', 'ELSS', 'SIP'
    ]

@app.route('/add', methods=['GET', 'POST'])
def add_transaction():
    categories = get_categories()
    if request.method == 'POST':
        category = request.form['category']
        description = request.form['description']
        amount = float(request.form['amount'])

        current_month = datetime.datetime.now().month
        current_year = datetime.datetime.now().year

        existing_record = Transaction.query.filter_by(
            category=category,
            date=datetime.date(current_year, current_month, 1)
        ).first()

        if existing_record:
            existing_record.amount += amount
        else:
            new_transaction = Transaction(category=category, description=description, amount=amount)
            db.session.add(new_transaction)

        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('add_transaction.html', categories=categories)

def get_monthly_totals_by_category():
    transactions = Transaction.query.all()
    df = pd.DataFrame([(t.category, t.amount, t.date) for t in transactions], 
                      columns=['category', 'amount', 'date'])

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month

    monthly_totals = df.groupby(['year', 'month', 'category'])['amount'].sum().reset_index()
    category_totals = df.groupby('category')['amount'].sum()

    return monthly_totals, category_totals

@app.route('/update/<int:transaction_id>', methods=['GET', 'POST'])
def update_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    categories = get_categories()
    
    if request.method == 'POST':
        transaction.category = request.form['category']
        transaction.description = request.form['description']
        transaction.amount = float(request.form['amount'])
        db.session.commit()
        return redirect(url_for('index')) 
    
    return render_template('update_transaction.html', transaction=transaction, categories=categories)

@app.route('/delete/<int:transaction_id>', methods=['POST'])
def delete_transaction(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    db.session.delete(transaction)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/monthly_totals')
def monthly_totals():
    monthly_totals, category_totals = get_monthly_totals_by_category()
    return render_template('monthly_totals.html', monthly_totals=monthly_totals, category_totals=category_totals)

if __name__ == "__main__":
    app.run(debug=True)

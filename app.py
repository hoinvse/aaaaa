from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dữ liệu ví dụ, bạn có thể thay đổi theo nhu cầu của mình
transactions = []

@app.route('/')
def index():
    return render_template('index.html', transactions=transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    description = request.form.get('description')
    amount = float(request.form.get('amount'))
    transaction_type = request.form.get('transaction_type')

    transactions.append({
        'description': description,
        'amount': amount,
        'type': transaction_type
    })

    return redirect(url_for('index'))

@app.route('/edit_transaction/<int:index>', methods=['GET', 'POST'])
def edit_transaction(index):
    if request.method == 'GET':
        transaction = transactions[index]
        return render_template('edit_transaction.html', index=index, transaction=transaction)
    elif request.method == 'POST':
        description = request.form.get('description')
        amount = float(request.form.get('amount'))
        transaction_type = request.form.get('transaction_type')

        transactions[index] = {
            'description': description,
            'amount': amount,
            'type': transaction_type
        }

        return redirect(url_for('index'))

@app.route('/delete_transaction/<int:index>')
def delete_transaction(index):
    transactions.pop(index)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

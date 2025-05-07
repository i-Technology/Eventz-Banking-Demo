from eventzAPI import publish

def F_deposit(event):
    publish('TransactionApproved', {
        'amount': event['amount'],
        'account_uuid': event['account_uuid'],
        'resulting_balance': event['amount']
    })

# Example usage
if __name__ == "__main__":
    F_deposit({'account_uuid': 'acct123', 'amount': 100.0})

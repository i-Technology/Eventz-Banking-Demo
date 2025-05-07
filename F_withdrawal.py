from eventzAPI import publish, read_latest, decline


def F_withdrawal(event):
    acct = read_latest('AccountOpened', {'account_uuid': event['account_uuid']})
    if not acct or acct['status'] != 'open':
        return decline(event, reason='Account blocked or not found')
    if acct['balance'] < event['amount']:
        return decline(event, reason='Insufficient funds')

    new_balance = acct['balance'] - event['amount']
    publish('TransactionApproved', {
        'amount': event['amount'],
        'account_uuid': event['account_uuid'],
        'resulting_balance': new_balance
    })

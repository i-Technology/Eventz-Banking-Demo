from eventzAPI import publish, read_latest, decline

def F_card_payment(event):
    card = read_latest('CardIssued', {'card_uuid': event['card_uuid']})
    if not card or card['status'] != 'active':
        return decline(event, reason='Card not active or not found')

    acct = read_latest('AccountOpened', {'account_uuid': card['account_uuid']})
    if not acct or acct['status'] != 'open':
        return decline(event, reason='Account blocked or not found')
    if acct['balance'] < event['amount']:
        return decline(event, reason='Insufficient funds')

    new_balance = acct['balance'] - event['amount']
    publish('TransactionApproved', {
        'amount': event['amount'],
        'account_uuid': acct['account_uuid'],
        'resulting_balance': new_balance
    })

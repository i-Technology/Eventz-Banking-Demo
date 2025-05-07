from eventzAPI import publish

def F_block_account(event):
    publish('AccountBlocked', {
        'account_uuid': event['account_uuid']
    })

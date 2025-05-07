from eventzAPI import publish

def F_block_card(event):
    publish('CardBlocked', {
        'card_uuid': event['card_uuid']
    })

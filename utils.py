# Define a function to retrieve the accrued charges and balance from Linode
def get_charges(headers, requests, URL):
    response = requests.get(URL, headers=headers)
    accrued_charges = response.json()["balance_uninvoiced"]
    return accrued_charges


def get_balance(headers, requests, URL):
    response = requests.get(URL, headers=headers)
    balance = response.json()["balance"]
    return balance

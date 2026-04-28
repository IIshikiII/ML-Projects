import sys


def main() -> None:
    """The function that processes 3 lists of emails"""
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
               'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
               'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
                    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
                    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

    clients_set = set(clients)
    participants_set = set(participants)
    recipients_set = set(recipients)

    if check_args() == 1:
        raise Exception("Incorrect args count")
    elif check_args() == 2:
        raise Exception("Commant is not supported")
    else:
        for email in gen_set(clients_set, participants_set, recipients_set):
            print(email)


def check_args() -> int:
    """
    The function that checks input
    0 - Ok
    1 - incorrect args count
    2 - commant is not supported
    """

    if len(sys.argv) != 2:
        res = 1
    elif sys.argv[1] not in {'call_center', 'potential_clients', 'loyalty_program'}:
        res = 2
    else:
        res = 0
    return res


def gen_set(clients_set: set, participants_set: set, recipients_set: set) -> set:
    """
    The function that generate:
    1 - list of clients who have not seen your promotional email yet. 
    2 - list of participants who are not your clients.
    3 - list of clients who did not participate in the event.
    """
    if sys.argv[1] == 'call_center':
        res = clients_set - recipients_set
    elif sys.argv[1] == 'potential_clients':
        res = participants_set - clients_set
    elif sys.argv[1] == 'loyalty_program':
        res = clients_set - participants_set
    return res


if __name__ == "__main__":
    main()

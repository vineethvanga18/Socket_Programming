# import socket programming library
import sys
import socket
import multiprocessing


# Checks for precedence of operators
def precedence(operator):
    if operator == '+' or operator == '-':
        return 1
    if operator == '*' or operator == '/':
        return 2
    return 0


# Performs arithmetic operations
def Perform_Operation(a, b, operator):
    if operator == '+':
        return a + b
    if operator == '-':
        return a - b
    if operator == '*':
        return a * b
    if operator == '/':
        return a / b


# Evaluates the given query
def evaluate(query):
    # Stores local results in the form of stack
    Operands = []

    # Stores operators in the form of stack
    Operators = []

    try:
        i = 0
        while i < len(query):

            # Skips whitespaces
            if query[i] == ' ':
                i += 1
                continue

            # Pushes digits into Operands
            elif query[i].isdigit():
                Operand = 0

                while i < len(query) and query[i].isdigit():
                    Operand = (Operand * 10) + int(query[i])
                    i += 1

                i -= 1

                Operands.append(Operand)

            # Takes care of negative numbers
            elif query[i] == '-' and i < len(query) - 1 and query[i+1].isdigit():
                Operand = 0
                i += 1
                while i < len(query) and query[i].isdigit():
                    Operand = (Operand * 10) + int(query[i])
                    i += 1

                i -= 1

                Operands.append(-1*Operand)

            # If an Operator is found
            else:

                while len(Operators) != 0 and precedence(Operators[-1]) >= precedence(query[i]):
                    val2 = Operands.pop()
                    val1 = Operands.pop()
                    Operator = Operators.pop()

                    Operands.append(Perform_Operation(val1, val2, Operator))

                Operators.append(query[i])

            i += 1

        # Now that entire query has been parsed, perform any left out Operations
        while len(Operators) != 0:
            val2 = Operands.pop()
            val1 = Operands.pop()
            Operator = Operators.pop()

            Operands.append(Perform_Operation(val1, val2, Operator))

        # Top of Operands contains result, return it
        return Operands[-1]
    except IndexError:
        return "Please enter a Non-Empty and Valid query"


# target function where process operations run
def process(connection, client_id):
    # Now that a connection is established, respond to queries from client
    while True:
        # Waiting to receive a query from client
        query = connection.recv(1024)

        # if client exits, close the Connection and end the process
        if not query:
            print('client', client_id, 'Disconnected')
            connection.close()
            sys.exit()
        else:
            # formatting the query to string from bytes
            query = str(query, 'utf-8').strip('\n')

            # Evaluating the query from client
            print('client', client_id, 'sent a query :', query)
            result = evaluate(query)

            # Send back the result to client
            connection.send(str(result).encode('ascii'))


def main():
    # Server listens on all local IP addresses
    host = ""

    # Getting port from Command line, if not supplied fallback to 8000
    try:
        port = int(sys.argv[1])
    except IndexError:
        port = 5000

    total_clients_connected = 0
    # Creating a Socket object with AF_NET(IPv4 address family) and SOCK_STREAM(TCP socket)
    Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Binding Socket to port
    print("socket bound to port", port)
    Socket.bind((host, port))

    # Put the Socket into listening mode(Become a server Socket)
    print("socket is listening")
    Socket.listen(5)

    while True:
        # Accepting connection from client and creating a Connection object (for Communication with client)
        Connection, Address = Socket.accept()
        total_clients_connected += 1
        print('Connected with client ', total_clients_connected)

        # Start a new Process for every client connected
        Process = multiprocessing.Process(target=process, args=(Connection, total_clients_connected))
        Process.start()


if __name__ == '__main__':
    main()

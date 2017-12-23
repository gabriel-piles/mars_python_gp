from communication_center import *

if __name__ == '__main__':
    try:
        communications = CommunicationCenter()
        #path = input("Commands file path: ")
        if communications.execute_commands_from_file('commands_example.txt'):
            print(communications)
    except CustomError as exception_value:
        print(exception_value)

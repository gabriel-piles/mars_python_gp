from communication_center import CommunicationCenter

if __name__ == '__main__':
    communications = CommunicationCenter()
    path = input("Commands file path: ")
    if communications.execute_commands_from_file(path):
        print(communications)

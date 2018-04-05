import csv
import getpass
import vk_api

MAGIC_CONST = 2000000000


def main():
    print('VK messages grabber')
    logged_in = False
    while not logged_in:
        login = input('Login: ')
        password = getpass.getpass('Password: ')
        vk_session = vk_api.VkApi(login, password)

        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            print(error_msg)
            continue

        logged_in = True

    tools = vk_api.VkTools(vk_session)

    while True:
        messages_type = int(input('What do you want to download? 1 - user dialog, 2 - chat, 0 - exit: '))
        if messages_type == 0:
            return
        if messages_type == 1:
            chat_id = int(input('ID of dialog: '))
        elif messages_type == 2:
            chat_id = int(input('ID of chat: ')) + MAGIC_CONST
        else:
            continue

        messages = tools.get_all('messages.getHistory', 200, {'peer_id': chat_id})

        print('Messages count:', messages['count'])

        with open(f'messages{str(chat_id)}.csv', 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['id', 'user_id', 'from_id', 'body', 'date'])
            for message in messages['items']:
                try:
                    writer.writerow([str(message['id']), str(message['user_id']), str(message['from_id']), str(message['body']), str(message['date'])])
                except:
                    pass
        pass


if __name__ == '__main__':
    main()

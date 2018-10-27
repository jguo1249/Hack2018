from twilio.rest import Client
from dateutil import parser

from ndq.db import TOPIC_LIST
from ndq.user import get_attribute


###GENERAL INFO###

account_sid = 'ACbbf3703e6d7faeb202cd33629b4708fc'
auth_token = '534c5bf0bf485062e6fca35218736528'
client = Client(account_sid, auth_token)
from_number = '+16147050284'


########################################## HELPER FUNCTIONS ######################################
def has_number(string):
    words = string.split()
    for i in words:
        if i.isdigit():
            return i
    return None

def remove_topics(number,remove_list):
    pass
    #DB stuff

def add_topics(number,add_list):
    pass
    #DB stuff

def set_attribute(number,context):
    pass
    #DB stuff

def set_summary_length(number,length):
    pass
    #DB stuff

def set_delivery_time(number,epoch_time):
    pass
    #DB stuff

def set_frequency(number,frequency):
    pass
    #DB stuff

############################################ MAIN FUNCTIONS ######################################


## Should be accompanied with adding number to db
def twilio_signup(number):
    try:
        message = client.messages \
            .create(
                 body='''Welcome to News Done Quick! Thank you for subscribing to our service.

Text help for options and unsubscribe to unsubscribe.''',
                 from_= from_number,
                 to = number
             )
        print(message.sid)
        return {"success":"true"}
    except Exception as e:
        print(e)
        return {"success":"false"}


def send_data(data,number):
    try:
        message = message = client.messages \
            .create(
                 body=data,
                 from_= from_number,
                 to = number
             )
        print(message.sid)
        return {"success":"true"}
    except Exception as e:
        print(e)
        return {"success":"false"}


## Need history list with message added into it
def process_info(message, number):
    try:
        message = message.lower()
        context = get_attribute(number, 'context')

        if 'help' in message:
            send_data("""What would you like to do?

* My current settings
* Change frequency
* Change delivery time
* Change summary lengths
* Change topics
""", number)

        elif 'change' in message and 'frequency' in message and (context != 'topics' and context != 'add topic' and context != 'remove topic' and context != 'time' and context != 'summary'):
            send_data('What would you like the new frequency to be (in hours)?',number)
            set_attribute(number, 'context', 'frequency')

        elif has_number(message) and context == 'frequency':
            set_frequency(number,has_number(message))
            send_data('Your frequency is now set to ' + has_number(message) + ' hours',number)
            set_attribute(number, 'context', '')

        elif 'change' in message and 'time' in message and (context != 'topics' and context != 'add topic' and context != 'remove topic' and context != 'frequency' and context != 'summary'):
            send_data('What would you like the new delivery time to be?',number)
            set_attribute(number, 'context', 'time')

        elif context == 'time':
            try:
                std_time = parser.parse(message)
                epoch = std_time.timestamp()
                set_time(number,epoch)

                send_data('Your deivery time is now set to ' + message,number)
                set_attribute(number, 'context', '')

            except Exception as e:
                print(e)
                send_data("I'm sorry but I don't understand the time you have input",number)

        elif 'change' in message and ('summary' in message or 'length' in message) and (context != 'topics' and context != 'add topic' and context != 'remove topic' and context != 'time' and context != 'frequency'):
            send_data('How many sentences would you like the summary to contain? (maximum 8)',number)
            set_attribute(number, 'context', 'summary')

        elif context == 'summary':
            try:
                num_sentences = int(has_number(message))
                if num_sentences <= 8:
                    set_summary_length(number,has_number(message))
                    send_data('Your summary length is now set to ' + has_number(message) + ' sentences',number)
                    set_attribute(number, 'context', '')
                elif num_sentences > 8:
                    send_data('A maximum of 8 sentences is allowed',number)
            except Exception as e:
                print(e)
                send_data("I'm sorry but that dosen't make sense",number)


        elif 'change' in message and 'topic' in message and context != 'frequency' and context != 'time' and context != 'summary':
            send_data('Would you like to add a topic or remove a topic?',number)
            set_attribute(number, 'context', 'topics')


        elif 'add' in message and 'topic' in message and context != 'frequency' and context != 'time' and context != 'summary':
            topics_to_add = '''Which of the following topics would you like to add:

'''
            remaining = TOPIC_LIST - topics_set
            if len(remaining)>0:
                for i in remaining:
                    topics_to_add += '* ' + i + '\n'
                topics_to_add = topics_to_add
                set_attribute(number, 'context', 'add topic')
            else:
                topics_to_add = 'You are currently subscribed to all topics'
            send_data(topics_to_add,number)

        elif 'remove' in message and 'topic' in message and context != 'frequency' and context != 'time' and context != 'summary':
            topics_to_remove = '''Which of the following topics would you like to remove:

'''
            if len(topics_set)>0:
                for i in topics_set:
                    topics_to_remove += '* ' + i + '\n'
                topics_to_remove = topics_to_remove
                set_attribute(number, 'context', 'remove topic')
            else:
                topics_to_remove = 'You are currently subscribed to zero topics'
            send_data(topics_to_remove,number)

        elif context == 'remove topic':
            remove_list = []
            for i in TOPIC_LIST:
                if i.lower() in message:
                    remove_list.append(i)
            if len(remove_list)>0:
                data_str = "Removed topics "
                for i in remove_list:
                    data_str += i + ', '
                data_str = data_str[:-2]
                send_data(data_str,number)
                remove_topics(number,list(TOPIC_LIST-set(remove_list)))
                set_attribute(number, 'context', '')
            else:
                send_data("I'm sorry but I don't understand the topics you sent",number)

        elif context == 'add topic':
            add_list = []
            for i in TOPIC_LIST:
                if i.lower() in message:
                    add_list.append(i)
            if len(add_list)>0:
                data_str = "Added topics "
                for i in add_list:
                    data_str += i + ', '
                data_str = data_str[:-2]
                send_data(data_str,number)
                add_topics(number,add_list)
                set_attribute(number, 'context', '')
            else:
                send_data("I'm sorry but I don't understand the topics you sent",number)

        elif 'unsubscribe' in message:
            set_attribute(number, 'context', 'unsubscribed')
            send_data("We're sorry to see you go",number)

        else:
            send_data("""I'm sorry but I'm a little lost right now.
Could we start over?""",number)
            set_attribute(number, 'context', '')

        return {"success":"true"}

    except Exception as e:
        print(e)
        return {"success":"false"}


#Testing
'''
twilio_signup('+16142706290')
process_info('help','+16142706290')
process_info('change frequency','+16142706290')
process_info('6 hours','+16142706290')
process_info('change time','+16142706290')
process_info('12 PM','+16142706290')
process_info('change summary length','+16142706290')
process_info('45','+16142706290')
process_info('8','+16142706290')
process_info('change topic','+16142706290')
process_info('add topic','+16142706290')
process_info("Sports, Local",'+16142706290')
process_info('remove topic','+16142706290')
process_info("Sports, Local",'+16142706290')
process_info("unsubscribe",'+16142706290')
'''

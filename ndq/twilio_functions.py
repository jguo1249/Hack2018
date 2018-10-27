from twilio.rest import Client


###GENERAL INFO###

account_sid = 'ACbbf3703e6d7faeb202cd33629b4708fc'
auth_token = '534c5bf0bf485062e6fca35218736528'
client = Client(account_sid, auth_token)
from_number = '+16147050284'
all_topics = set(['World','Local','Sports','Science','Food','Entertainment','Politics','Technology'])


##########################################HELPER FUNCTIONS######################################
def has_number(string):
    words = string.split()
    for i in words:
        if i.isdigit():
            return i
    return None

############################################MAIN FUNCTIONS######################################


## Should be accompanied with adding number to db
def twilio_signup(number):
    try:
        message = client.messages \
            .create(
                 body='''Welcome to News Done Quick! Thank you for subscribing to our service

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
def process_info(message,number,topics,context):
    topics_set = set(topics)
    message = message.lower()

    if 'help' in message:
        send_data("""What would you like to do?

* Change frequency
* Change topics
""", number)
        
    elif 'change' in message and 'frequency' in message and (context != 'topics' and context != 'add topic' and context != 'remove topic'):
        send_data('What would you like the new frequency to be (in hours)?',number)
        ## set_context('frequency',number)

    elif has_number(message) and context == 'frequency':
        ## change_frequency(has_number(message),number)
        send_data('Your frequency is now set to ' + has_number(message) + ' hours',number)
        ## set_context('',number)
    
        
    elif 'change' in message and 'topic' in message and context != 'frequency':
        send_data('Would you like to add a topic or remove a topic?',number)
        ## set_context('topics',number)

        
    elif 'add' in message and 'topic' in message and context != 'frequency':
        topics_to_add = '''Which of the following topics would you like to add:

'''
        remaining = all_topics - topics_set
        if len(remaining)>0:
            for i in remaining:
                topics_to_add += '* ' + i + '\n'
            topics_to_add = topics_to_add
            ## set_context('add topic',number)
        else:
            topics_to_add = 'You are currently subscribed to all topics'
        send_data(topics_to_add,number)

    elif 'remove' in message and 'topic' in message and context != 'frequency':
        topics_to_remove = '''Which of the following topics would you like to remove:

'''
        if len(topics_set)>0:
            for i in topics_set:
                topics_to_remove += '* ' + i + '\n'
            topics_to_remove = topics_to_remove
            ## set_context('remove topic',number)
        else:
            topics_to_remove = 'You are currently subscribed to zero topics'
        send_data(topics_to_remove,number)

    elif context == 'remove topic':
        remove_list = []
        for i in all_topics:
            if i.lower() in message:
                remove_list.append(i)
        if len(remove_list)>0:
            data_str = "Removed topics "
            for i in remove_list:
                data_str += i + ', '
            data_str = data_str[:-2]
            send_data(data_str,number)
            ## remove_topics_db(remove_list[],number)
            ## set_context('',number)
        else:
            send_data("I'm sorry but I don't understand the topics you sent",number)

    elif context == 'add topic':
        add_list = []
        for i in all_topics:
            if i.lower() in message:
                add_list.append(i)
        if len(add_list)>0:
            data_str = "Added topics "
            for i in add_list:
                data_str += i + ', '
            data_str = data_str[:-2]
            send_data(data_str,number)
            ## add_topics_db(add_list[],number)
            ## set_context('',number)
        else:
            send_data("I'm sorry but I don't understand the topics you sent",number)

    elif 'unsubscribe' in message:
        ## set_context('unsubscribed',number) maybe just delete the object?
        send_data("We're sorry to see you go",number)

    else:
        send_data("""I'm sorry but I'm a little lost right now
        Could we start over?""",number)
        ## set_context('',number)

    

    return


#Testing
twilio_signup('+16142706290')
process_info('help','+16142706290',[],'')
process_info('change frequency','+16142706290',[],'')
process_info('6 hours','+16142706290',[],'frequency')
process_info('change topic','+16142706290',[],'')
process_info('add topic','+16142706290',[],'topics')
process_info("Sports, Local",'+16142706290',[],'add topic')
process_info('remove topic','+16142706290',['Sports','Local'],'')
process_info("Sports, Local",'+16142706290',['Sports','Local'],'remove topic')
process_info("unsubscribe",'+16142706290',[],'')
        

    











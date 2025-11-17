import os

def get_operational(call, bot):
    message_text = (
        "Чек-лист РЦ:\n"
        "https://docs.google.com/forms/d/e/1FAIpQLSeCUmyt0Xc4jHNJ9ez2gwLzobneIw2LibMJ4InTtJoC_Cc8hg/viewform\n\n"
        "Чек-лист магазину:\n"
        "https://forms.gle/QEEZLcPM9iJjb6Lp7\n"
        "https://docs.google.com/spreadsheets/d/181RYCpcl5_QKJ7WHyyjQ50ef_uJzU24P0IDC5ZbIYQg/edit#gid=2022098910\n\n"
        "Чек-лист менеджер:\n"
        "https://forms.gle/3JdwaWUnAPnQab849\n"
        "https://docs.google.com/spreadsheets/d/1zITMg2BaRNvXZpR0Q4dCp-tBSyXVCE-qGwR2rJfB5S8/edit?resourcekey#gid=1097342196\n\n"
        "Чек-лист менеджера Тімірязєва-12б:\n"
        "https://forms.gle/RuMnMbYJDE3JVpeb8\n"
        "https://docs.google.com/spreadsheets/d/1QZdLLkbhbhlYkeZ40yuCOz5UCTJ6l4QcbjgK2inD9c8/edit?resourcekey#gid=219982839\n\n"
        "Чек-лист магазину Тімірязєва-12б:\n"
        "https://forms.gle/r3fsLNMxmZYUaxY36\n"
        "https://docs.google.com/spreadsheets/d/1QZdLLkbhbhlYkeZ40yuCOz5UCTJ6l4QcbjgK2inD9c8/edit?resourcekey#gid=219982839\n\n"
        "Чек-лист пекарні:\n"
        "https://forms.gle/r3fsLNMxmZYUaxY36\n"
        "https://docs.google.com/spreadsheets/d/1QZdLLkbhbhlYkeZ40yuCOz5UCTJ6l4QcbjgK2inD9c8/edit?resourcekey#gid=219982839\n"
    )
    bot.send_message(call.message.chat.id, message_text)

def get_documents(call, bot):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)

    file_1_path = os.path.join(parent_dir, 'files', 'списання.xlsx')
    file_2_path = os.path.join(parent_dir, 'files', 'службова (дорога).docx')
    file_3_path = os.path.join(parent_dir, 'files', 'протерміновка.xlsx')

    with open(file_1_path, 'rb') as file_1:
        bot.send_document(call.message.chat.id, file_1)

    with open(file_2_path, 'rb') as file_2:
        bot.send_document(call.message.chat.id, file_2)

    with open(file_3_path, 'rb') as file_3:
        bot.send_document(call.message.chat.id, file_3)

def get_operator(call, bot):
    message_text = (
        "Гугл диск СБ:\n"
        "https://drive.google.com/drive/my-drive\n\n"
        "Чек-лист магазину:\n"
        "https://docs.google.com/spreadsheets/d/17oXUoBVZ2YzGn9Urnb1S1zfKBP8ISt_tcBHCfAeBn_s/edit?gid=1262384048#gid=1262384048\n\n"
        "Зловживання працівників:\n"
        "https://docs.google.com/spreadsheets/d/13yAl_IVZ8EQmnH0QDUZhCAG4059_ntWCuqegP5EYNe4/edit#gid=1882209401\n\n"
        "Графіки роботи магазинів:\n"
        "https://drive.google.com/drive/folders/1-4XhgndS2oH_HDHc9UHF521raijsFnpE\n\n"
    )
    bot.send_message(call.message.chat.id, message_text)
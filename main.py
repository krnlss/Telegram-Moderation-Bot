import time
import keep_alive
from aiogram import executor, types
from aiogram.dispatcher.filters import AdminFilter, IsReplyFilter

from config import adminId
from random import randint
from misc import bot, dp

keep_alive.keep_alive()

# Send admin message about bot started
async def send_adm(dp):
    await bot.send_message(chat_id=adminId, text='Pascal Initialized')


# info tour
@dp.message_handler(commands=['start'])
async def welcome_send_info(message: types.Message):
    await message.answer(f"{message.from_user.full_name}, Hello 😊\n"
                         f"Pascal is a chat moderation bot developed by @zwexii\n"
                         f" Admin permissions are required for the bot to function!\n\n"
                         f"⚒ Admin commands:\n"
                         f"<code>!ban</code> (reason) - Bans a specified guild member.\n"
                         f"<code>!mute 15m</code> (30m, 1h, 6h, 1d) - Mutes a specified guild member\n"
                         f"<code>!unmute</code> - Unmutes a user\n"
                         f"<code>!del</code> - Deletes a message\n"
                         f"<code>!pin</code> - Pins a message\n"
                         f"<code>!unpin</code> - Unpins a message\n"
                         f"<code>!me</code> - Get user info\n"
                         f"All commands except the latter should be replied to the user for them to work! \n"
                         f"Bot by @zwexii|Dm for help 😉")


# new chat member
@dp.message_handler(content_types=["new_chat_members"])
async def new_chat_member(message: types.Message):
    chat_id = message.chat.id
    await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
    await bot.send_message(chat_id=chat_id, text=f"[{message.new_chat_members[0].full_name}]"
                                                 f"(tg://user?id={message.new_chat_members[0].id})"
                                                 f" Welcome to the server 😄 Make sure to follow the rules (Check Pins!)🤜! \n"
                                                 f"Bot By @zwexii", parse_mode=types.ParseMode.MARKDOWN)


# delete message user leave chat
@dp.message_handler(content_types=["left_chat_member"])
async def leave_chat(message: types.Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    


# user get info about him
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['me'],
commands_prefix='!/')
async def welcome(message: types.Message):
    if message.from_user.username is None:
        await message.reply(f"Name - {message.from_user.full_name}\nID - {message.from_user.id}\n")
    else:
        await message.reply(f"Name - {message.from_user.full_name}\n"
                            f"ID - <code>{message.from_user.id}</code>\n"
                            f"Username - @{message.from_user.username}\n")


# ban user
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True), commands=['ban'],
                    commands_prefix='!/', chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def ban(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    admin_id = message.from_user.id
    await bot.kick_chat_member(chat_id=message.chat.id, user_id=replied_user)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(chat_id=message.chat.id, text=f"[{message.reply_to_message.from_user.full_name}]"
                                                         f"(tg://user?id={replied_user})"
                                                         f" Was banned by [{message.from_user.full_name}]"
                                                         f"(tg://user?id={admin_id})",
                           parse_mode=types.ParseMode.MARKDOWN)


# mute user in chat
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True), commands=['mute'],
                    commands_prefix='!/', chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def mute(message: types.Message):
    args = message.get_args()
    if args:
        till_date = message.text.split()[1]
    else:
        till_date = "15m"

    if till_date[-1] == "m":
        ban_for = int(till_date[:-1]) * 60
    elif till_date[-1] == "h":
        ban_for = int(till_date[:-1]) * 3600
    elif till_date[-1] == "d":
        ban_for = int(till_date[:-1]) * 86400
    else:
        ban_for = 15 * 60

    replied_user = message.reply_to_message.from_user.id
    now_time = int(time.time())
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=replied_user, can_send_messages=False,
                                   can_send_media_messages=False, can_send_other_messages=False,
                                   until_date=now_time + ban_for)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(text=f"[{message.reply_to_message.from_user.full_name}](tg://user?id={replied_user})"
                                f" muted for {till_date}",
                           chat_id=message.chat.id, parse_mode=types.ParseMode.MARKDOWN)


# random mute chat member
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['dont_click_me'],
commands_prefix='!/')
async def mute_random(message: types.Message):
    now_time = int(time.time())
    replied_user_id = message.from_user.id
    replied_user = message.from_user.full_name
    random_m = randint(1, 10)
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=replied_user_id, can_send_messages=False,
                                   can_send_media_messages=False, can_send_other_messages=False,
                                   until_date=now_time + 60 * random_m)
    await bot.send_message(text=f"[{replied_user}](tg://user?id={replied_user_id})"
                                f" has been muted for {random_m} minutes",
                           chat_id=message.chat.id, parse_mode=types.ParseMode.MARKDOWN)


# unmute user in chat
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True), commands_prefix='!/',
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['unmute'])
async def unmute(message: types.Message):
    replied_user = message.reply_to_message.from_user.id
    await bot.restrict_chat_member(chat_id=message.chat.id, user_id=replied_user, can_send_messages=True,
                                   can_send_media_messages=True, can_send_other_messages=True)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await bot.send_message(text=f"[{message.reply_to_message.from_user.full_name}](tg://user?id={replied_user})"
                                f" has been unmuted",
                           chat_id=message.chat.id, parse_mode=types.ParseMode.MARKDOWN)


# pin chat message
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True),
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['pin'], commands_prefix='!/')
async def pin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.pin_chat_message(message_id=msg_id, chat_id=message.chat.id)


# unpin chat message
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True), commands_prefix='!/',
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['unpin'])
async def unpin_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.unpin_chat_message(message_id=msg_id, chat_id=message.chat.id)

# delete user message
@dp.message_handler(AdminFilter(is_chat_admin=True), IsReplyFilter(is_reply=True), commands_prefix='!/',
                    chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['del'])
async def delete_message(message: types.Message):
    msg_id = message.reply_to_message.message_id
    await bot.delete_message(chat_id=message.chat.id, message_id=msg_id)
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


# get chat admins list
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['admins'],
                    commands_prefix='!/')
async def get_admin_list(message: types.Message):
    admins_id = [(admin.user.id, admin.user.full_name) for admin in await bot.get_chat_administrators(
        chat_id=message.chat.id)]
    admins_list = []
    for ids, name in admins_id:
        admins_list.append("".join(f"[{name}](tg://user?id={ids})"))
    result_list = ""
    for admins in admins_list:
        result_list += "".join(admins) + '\n'
    await message.reply("Admins :\n" + result_list, parse_mode=types.ParseMode.MARKDOWN)


# report about spam or something else
@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], commands=['report'],
                      commands_prefix='!/')
async def report_by_user(message: types.Message):
    msg_id = message.reply_to_message.message_id
    user_id = message.from_user.id
    admins_list = [admin.user.id for admin in await bot.get_chat_administrators(chat_id=message.chat.id)]
    for adm_id in admins_list:
        try:
            await bot.send_message(text=f"User: [{message.from_user.full_name}](tg://user?id={user_id})\n"
                                        f"Reported:\n"
                                        f"[Reported a possible violation](t.me/{message.chat.username}/{msg_id})",
                                   chat_id=adm_id, parse_mode=types.ParseMode.MARKDOWN,
                                   disable_web_page_preview=True)
        except:
            pass
    await message.reply("Message has been reported")


# # delete links and tags from users, allow for admins
@dp.message_handler(content_types=['text'])
async def delete_links(message: types.Message):
  Admin = 5024343498
  MY_CHANNEL = message.chat.id
  if 'fuck' in message.text:             
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)
  if 'stfu' in message.text:
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)
            
  if 'nigga' in message.text:
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)             
  if 'faggot' in message.text:
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)              
  if 'nigger' in message.text:
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)              
  if 'bitch' in message.text:
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)             
  if 'shit' in message.text:
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)
  if 'uwu' in message.text:
            await bot.send_message(MY_CHANNEL,f"Message from @{message.from_user.username} contained blacklisted words 😡")
            await bot.send_message(Admin,f"Message from user:\n@{message.from_user.username}:<code>{message.from_user.id}</code>\nContained blacklisted words")
            await bot.delete_message(message.chat.id, message.message_id)        
# Polling
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=send_adm, skip_updates=True)

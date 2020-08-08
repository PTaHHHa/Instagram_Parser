import requests
from telegram.ext import Updater, CommandHandler
"""This is my script in form of Telegram Bot"""

updater = Updater(token='1285701260:AAEFpFQ43WtA7lMEjyjBHhw0VwV5LxomeCU', use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    username = ' '.join(context.args)
    if username == '':
        update.message.reply_text("Welcome to Instagram public API parser bot. "
                                  "To start working with bot use /start with username")
    else:
        update.message.reply_text(f'Fetching information about {username}')
        context.user_data['username'] = username
        user_url = f'https://www.instagram.com/{username}'
        context.user_data['user_url'] = user_url
        request = requests.get(user_url + '/?__a=1')
        if request.status_code == 404:
            update.message.reply_text('Username is invalid')
        else:
            json_file = request.json()
            context.user_data['json_file'] = json_file
            update.message.reply_text('Use commands /userdata or /latestposts to get information about user')


def get_user_data(update, context):
    if context.args:
        print('Arguments are not supported')
    username = context.user_data['username']
    user_url = context.user_data['user_url']
    json_file = context.user_data['json_file']
    profile_image = json_file['graphql']['user']['profile_pic_url_hd']
    user_status = json_file['graphql']['user']['biography']
    followers = json_file['graphql']['user']['edge_followed_by']['count']
    posts_number = json_file['graphql']['user']['edge_owner_to_timeline_media']['count']
    update.message.reply_text(f'{profile_image}\n\n Profile: {user_url}\n Username: {username} \n '
                              f'User profile status: {user_status} \n Followers: {followers} \n'
                              f' Number of posts: {posts_number}')
    update.message.reply_text("Use command /latestposts to get information about user's posts\n or "
                              "/start <username> to get information about another user")


def get_post_data(update, context):
    json_file = context.user_data['json_file']
    username = context.user_data['username']
    post_list = json_file['graphql']['user']['edge_owner_to_timeline_media']['edges']
    if not post_list:
        update.message.reply_text(f"{username} don't have any posts."
                                  f"\n\nUse command /userdata to get information about user's profile \nor "
                                  "/start <username> to get information about another user")
    else:
        url = [f'https://www.instagram.com/{username}/p/{post["node"]["shortcode"]}' for post in post_list]
        likes = [post['node']['edge_liked_by']['count'] for post in post_list]
        comment = [post['node']['edge_media_to_comment']['count'] for post in post_list]
        update.message.reply_text('Here is information about last 12 posts')
        for url, likes, comment in zip(url, likes, comment):
            update.message.reply_text(f'Url: {url} \nLikes: {likes} \nComments: {comment}')
        update.message.reply_text("Use command /userdata to get information about user's profile \n or "
                                  "/start <username> to get information about another user")


start_handler = CommandHandler('start', start, pass_chat_data=True)
get_user_data = CommandHandler('userdata', get_user_data)
get_post_data = CommandHandler('latestposts', get_post_data)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(get_user_data)
dispatcher.add_handler(get_post_data)
updater.start_polling()
updater.idle()

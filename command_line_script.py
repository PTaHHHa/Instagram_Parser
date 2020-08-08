import sys
import requests
"""This is my script in form of Command line script"""


def get_user_data(json_file, argv):
    print('User data')
    user_status = json_file['graphql']['user']['biography']
    followers = json_file['graphql']['user']['edge_followed_by']['count']
    posts_number = json_file['graphql']['user']['edge_owner_to_timeline_media']['count']
    print(posts_number)


def get_post_data(json_file, argv):
    post_list = json_file['graphql']['user']['edge_owner_to_timeline_media']['edges']
    url = [f'https://www.instagram.com/{argv}/p/{post["node"]["shortcode"]}' for post in post_list]
    likes = [post['node']['edge_liked_by'] for post in post_list]
    comment = [post['node']['edge_media_to_comment']['count'] for post in post_list]
    return print(comment)


def request_json(argv, arg):
    request = requests.get(f'https://www.instagram.com/{argv}/?__a=1')
    if request.status_code == 404:
        print('Username is invalid')
    else:
        json_file = request.json()
        if arg == 'get_post_data':
            return get_post_data(json_file, argv)
        elif arg == 'get_user_data':
            return get_user_data(json_file, argv)
        else:
            print('Wrong function input')


def main(argv=None):
    if argv is None:
        argv = str(sys.argv[1])
        arg = str(sys.argv[2])
        request_json(argv, arg)


if __name__ == '__main__':
    main()

import sys
import requests
import json


def get_post_data(json_file, argv):
    post_list = json_file['graphql']['user']['edge_owner_to_timeline_media']['edges']
    url = [f'https://www.instagram.com/{argv}/p/{post["node"]["shortcode"]}' for post in post_list]
    likes = [post['node']['edge_liked_by'] for post in post_list]
    comment = [post['node']['edge_media_to_comment']['count'] for post in post_list]
    return print(comment)


def request_json(argv):
    request = requests.get(f'https://www.instagram.com/{argv}/?__a=1')
    if request.status_code == 404:
        print('Username is invalid')
    else:
        json_file = request.json()
        return get_post_data(json_file, argv)


def main(argv=None):
    if argv is None:
        argv = str(sys.argv[1])
    request_json(argv)


if __name__ == '__main__':
    main()

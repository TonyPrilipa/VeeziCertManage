import requests

URL = 'https://auth.veezi.com/token'

def get_token(url):
    username = ''
    password = ''
    login_query = 'grant_type=password&username={0}&password={1}&client_id=vista_id1'.format(username, password)

    request = requests.get(url, data=login_query)

    return request.text


def write_html(html):
    file = open('start.html', 'w')
    file.write(html)
    file.close()


def some_func(some_arg):
    cos = 2
    pass

if __name__ == '__main__':
    html = vsg_login(URL)

    write_html(html)


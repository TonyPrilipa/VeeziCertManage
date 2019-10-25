import requests

URL = 'https://auth.veezi.com/token'

def get_token(url):
    username = 'sysadmin%40cinemaciti.od.ua'
    password = 'sysadmin7775'
    login_query = 'grant_type=password&username={0}&password={1}&client_id=vista_id1'.format(username, password)

    request = requests.get(url, data=login_query)

    return request.text


def write_html(html):
    file = open('start.html', 'w')
    file.write(html)
    file.close()


if __name__ == '__main__':
    html = vsg_login(URL)

    write_html(html)


import tools.sapi as sapi

def config():
    url = input('Link?\n')
    li_at = ''
    li_a = ''
    jsessionid = ''
    file_name = input('File name?\n')

    sapi.api(url, li_at, li_a, jsessionid, file_name)

config()
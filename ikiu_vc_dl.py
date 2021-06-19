from downloader import Downloader
import time
import re


def ikiu_download(user_name, password, pasted_urls):

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36',
    }

    login_data = {
        'anchor': '',
        'username': user_name,
        'password': password,
        'rememberusername': '0'
    }

    ikiu_downloader = Downloader('http://lms.ikiu.ac.ir/blocks/whc_backup/login.php',
                         'https://ac.aminidc.com',
    login_data, headers, headers)

    if not ikiu_downloader.login({'logintoken'}):
        return

    for url in pasted_urls:
        if re.match(r'https://ac\.aminidc\.com/(.*)/.*', url):
            filename=re.findall('recording=(\d+)&', url)[0]
            print('Downloading ' + filename + '...')
            ikiu_downloader.set_name_to_save(filename)
            ikiu_downloader.set_pasted_url(url)
            ikiu_downloader.set_cookies()
            if not ikiu_downloader.create_downlaod_link():
                continue
            ikiu_downloader.download_file()
            ikiu_downloader.save_file()
            ikiu_downloader.extract_zip_file()
            ikiu_downloader.convert_media()
            ikiu_downloader.download_other_files()
            print(filename + ' downloaded!')
        else:
            print('Wrong URL format')
            time.sleep(10)

    ikiu_downloader.remove_temp_directory()

if __name__ == '__main__':
    with open('info.txt', 'r') as f:
        lines = f.read().splitlines()
        user_name = lines[0]
        password = lines[1]
        ikiu_download(user_name, password, lines[2:])
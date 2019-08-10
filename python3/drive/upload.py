# -*- coding: UTF-8 -*-


from __future__ import print_function
import pickle
import os.path
import time
import re
import httplib2
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
from googleapiclient.http import MediaFileUpload

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s.%(msecs)03d %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

SCOPES = ['https://www.googleapis.com/auth/drive']


def service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build('drive', 'v3', credentials=creds, cache_discovery=False)


def main(target_url):
    headers = {'User-Agent':
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    flag = True
    while flag:
        try:
            resp = requests.get(target_url, headers=headers)
            flag = False
        except Exception as e:
            print(e)
            time.sleep(0.4)
    resp.encoding = 'gb18030'
    soup = BeautifulSoup(resp.text, 'html.parser')
    title = soup.title.string
    title = title.replace(u'[原创投稿]', '') \
        .replace(u'DD-CLUB', '') \
        .replace(u'達蓋爾的旗幟 草榴社區', '') \
        .replace(u'達蓋爾的旗幟 | 草榴社區', '') \
        .replace(u' -', '') \
        .replace(u't66y.com', '')

    title = re.sub('\[([^\[\]]*)\]', '', title).strip()
    print(title)
    drive_service = service()
    folder_id = mkdir(drive_service, title)
    for x in soup.findAll(name="input", attrs={"data-link": True}):
        print(x['data-src'])
        upload(drive_service, folder_id, download_img(x['data-src']))


def download_img(url):
    filename = url.split("/")[-1]
    # logging.info("文件名为: %s" % filename)
    with open(filename, 'wb') as f:
        # 以二进制写入的模式在本地构建新文件
        header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

        flag = True
        while flag:
            try:
                resp = requests.get(url, headers=header)
                flag = False
            except Exception as e:
                print(e)
                time.sleep(0.4)
        f.write(resp.content)
    return filename


def mkdir(service, name):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': ['1-dR88E5CvWpAhY2KEcwwt4RMZK7hXtby']
    }
    file = service.files().create(body=file_metadata,
                                  fields='id').execute()
    logging.info('mkdir, name=%s,id= %s' % (name, file.get('id')))
    return file.get('id')


def list(service):
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        logging.info('No files found.')
    else:
        logging.info('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))


def upload(drive_service, folder_id, filename):
    file_metadata = {
        'name': filename,
        'parents': [folder_id]
    }
    media = MediaFileUpload(filename,
                            mimetype='image/' + filename.split(".")[-1],
                            resumable=True)
    file = drive_service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
    logging.info('File ID: %s' % file)
    os.remove(filename)


if __name__ == '__main__':
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3586487.html')
    # main('https://cl.vttg.pw/htm_mob/1906/16/3563050.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3568793.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3575378.html')
    # main('https://cl.cfbf.xyz/htm_mob/1906/16/3561953.html')
    # main('https://cl.cfbf.xyz/htm_mob/1906/16/3562648.html')
    # main('https://cl.cfbf.xyz/htm_data/1907/16/3575038.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3571852.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3583571.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3579771.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3576446.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3590269.html')
    # main('https://cl.cfbf.xyz/htm_mob/1907/16/3591531.html')
    main('https://cl.cfbf.xyz/htm_mob/1907/16/3586699.html')

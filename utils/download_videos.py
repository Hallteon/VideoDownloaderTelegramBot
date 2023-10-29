import os
import yt_dlp
import time

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options


def download_wait(vid_id):
    while True:
        time.sleep(5)
        files = os.listdir(f'{os.path.dirname(__file__)}/videos/')

        for fname in files:
            if fname == f'{vid_id}.mp4' and os.path.getsize(f'{os.path.dirname(__file__)}/videos/{fname}') != 0:
                return


def download_zen_video(zen_url):
    options = Options()
    options.add_argument("--headless")
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", f'{os.path.dirname(__file__)}/videos/')
    driver = webdriver.Firefox(options=options)

    url = 'https://zenstat.ru/video/check/'
    driver.get(url)

    time.sleep(1)
    download_form = driver.find_element(By.XPATH, "//form[@id='download-form']")

    time.sleep(1)
    download_input = download_form.find_element(By.XPATH, "//input[@class='form-control']")
    download_input.send_keys(zen_url)

    time.sleep(1)
    download_btn = download_form.find_element(By.XPATH, "//button[@class='btn']")
    download_btn.click()

    download_result = WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, "//a[@id='download-btn']")))
    select_resolution = Select(WebDriverWait(driver, 1000).until(EC.element_to_be_clickable((By.XPATH, "//select[@id='resolutions']"))))
    select_resolution.select_by_value('426x240')
    download_result.click()

    video_name = driver.find_element(By.XPATH, "//div[contains(@class, 'download-result')]//div[contains(@class, 'title')]").text
    video_id = zen_url.split('/')[-1]

    download_wait(video_id)
    driver.quit()

    return {'video_name': video_name, 'file_name': f'{video_id}.mp4'}


def download_yt_vk_video(url, name='%(title)s'):
    ydl_opts = {
        'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480][ext=m4a]/bestvideo+bestaudio/best',
        'outtmpl': '{}{}.%(ext)s'.format('utils/videos/', name),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        downloaded_file_path = ydl.prepare_filename(info_dict)

    return {'video_name': downloaded_file_path.split('/')[-1].split('.')[0], 'file_name': downloaded_file_path.split('/')[-1]}


# print(download_yt_vk_video('https://www.youtube.com/watch?v=vqiAOv6EVvo'))
# print(download_zen_video('https://dzen.ru/video/watch/65284ae5816f970013faad0e'))
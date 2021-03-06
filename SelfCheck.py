from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from os import path

import chromedriver_autoinstaller as autoinstaller
import os
import time

from Data import UserData

# To Build : pyinstaller --icon=check_icon.ico --onefile SelfCheck.py

mainlink = 'https://hcs.eduro.go.kr'


def StartCheck(info):
    print('자가진단 시작')

    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # 크롬창 안 뜨게
    options.add_argument('window-size=1920x1080')
    options.add_argument('--disable-gpu')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument("lang=ko_KR")  # 한국어

    driver = webdriver.Chrome(executable_path=info.driverPath, options=options)
    # driver = webdriver.Chrome(info.driverPath) # 옵션 적용 안함

    try:
        print(f'사이트 접속중 : {mainlink}')

        driver.get(mainlink)

        ### Main ###
        driver.implicitly_wait(3)
        driver.find_element(By.ID, 'btnConfirm2').click()
        driver.implicitly_wait(3)

        ### Login ###
        input_text_common = driver.find_elements(By.CLASS_NAME, 'input_text_common')
        # 0 : 학교, 1 : 성명, 2 : 생년월일
        input_text_common[0].click()

        ### 학교 선택창 ###
        print('학교 선택중...')
        # 지역 선택
        tmp = info.cities + 1
        driver.find_element_by_xpath(
            f'//*[@id="softBoardListLayer"]/div[2]/div[1]/table/tbody/tr[1]/td/select/option[{tmp}]').click()
        # 학교급 선택
        tmp = info.school_level + 1
        driver.find_element_by_xpath(
            f'//*[@id="softBoardListLayer"]/div[2]/div[1]/table/tbody/tr[2]/td/select/option[{tmp}]').click()
        # 학교명 입력
        input_schoolName = driver.find_element(By.CLASS_NAME, 'searchArea')
        input_schoolName.send_keys(info.school_name)
        input_schoolName.send_keys(Keys.ENTER)
        driver.implicitly_wait(3)
        # 검색된 학교 선택
        driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a/p/a').click()
        # 선택 완료 버튼
        driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[2]/input').click()

        ### Login ###
        input_text_common[1].send_keys(info.name)
        input_text_common[2].send_keys(info.birth)
        driver.find_element(By.ID, 'btnConfirm').click()
        # driver.find_element(By.ID, 'btnConfirm').send_keys(Keys.ENTER)

        ### Password ###
        print('비밀번호 입력중...')
        driver.implicitly_wait(3)
        time.sleep(0.5)
        driver.find_elements(By.CLASS_NAME, 'input_text_common')[0].send_keys(info.password)
        driver.find_element(By.ID, 'btnConfirm').click()

        print('진단 창 불러오는 중...')
        time.sleep(1.7) # more sleep

        ### 진단 참여 창 ###
        driver.find_element(By.CLASS_NAME, 'btn').click()
        driver.implicitly_wait(3)

        ### SELF CHECK ###
        print('진단 체크중...')
        for i in range(1, 4):
            xpath = f'//*[@id="container"]/div/div/div[2]/div[2]/dl[{i}]/dd/ul/li[1]/label'
            driver.find_element_by_xpath(xpath).click()
        driver.find_element(By.ID, 'btnConfirm').click()
        driver.implicitly_wait(3)

    except NoSuchElementException:
        print('''
        사이트 구조가 변경된 것 같습니다.
        개발자에게 문의해주세요 :)
        19sunrin153@sunrint.hs.kr\n''')
        driver.quit()
        return
    except AttributeError:
        print('''
        정보가 잘못 입력된 것 같아요.
        info.json 파일을 열어서 정보를 확인하고 수정하거나,
        파일을 삭제하여 다시 생성해주세요 :)
        ''')
        driver.quit()
        return
    except BaseException as e:
        print()
        print(e, type(e))
        print('''
        사이트를 불러오는 중 오류가 발생했습니다.
        연속해서 자가진단을 진행해도 이 문구가 뜰 수 있습니다.
        
        또는 크롬 드라이버를 최신버전으로 업그레이드 해주세요.\n''')
        driver.quit()
        return

    i = 'confirm.png'
    if path.exists(i):
        os.remove(i)
    driver.save_screenshot(i)

    print(f'자가진단 완료! ({i})')

    # -> file is TOO large..
    # from PIL import Image
    # confirmImg = Image.open(i)
    # confirmImg.show()
    driver.quit()


# def CreateFile():
#     level = input('1: 유치원, 2: 초등학교, 3: 중학교, 4: 고등학교, 5: 특수학교\n(숫자 하나) >> ')
#     school = input('학교이름 (정확히) >> ')
#     name = input('이름 >> ')
#     birth = input('생년월일 (YYMMDD) >> ')
#     pw = input('로그인 비밀번호 (숫자 4자리) >> ')

#     with open('info.txt', 'w', encoding='utf8') as file:
#         info = [level + '\n', school + '\n', name + '\n', birth + '\n', pw + '\n', './chromedriver.exe\n']
#         file.writelines(info)


# def LoadFile():
#     with open('info.txt', 'r', encoding='utf8') as file:
#         return file.readlines()


# def AppendFile(text):
#     with open('info.txt', 'a', encoding='utf8') as file:
#         file.write(text)


def installDriver():
    try:
        driverPath = autoinstaller.install(cwd=True)
        # AppendFile(f'{driverPath}\n')
        print(f'드라이버 설치 완료 (다운로드 경로 : {driverPath})\n')
        return True, driverPath

    except Exception as e:
        print(e)
        print('설치 중 문제가 생겼습니다 :( 다시 시도해주세요.')
        return False, ''


# def Main():
#     if path.exists('./info.txt'):

#         info = LoadFile()
#         chromeDriverPath = info[len(info) - 1][:-1]  # 마지막줄

#         if not path.exists(chromeDriverPath):  # 크롬드라이버 파일이 존재하지 않을 때
#             a = input('\n크롬드라이버가 존재하지 않습니다.\n자동으로 최신버전을 다운받으시겠습니까? (y/n) : ')

#             if a in 'yY':
#                 success, chromeDriverPath = installDriver()
#                 if not success:
#                     return
#             else:
#                 print('\n크롬드라이버를 실행파일과 같은 폴더에 설치해주세요. (https://github.com/XxCtrlZxX/SelfCheck 참고)\n')
#                 return

#         level, school, name, birth, pw = info[0][:-1], info[1][:-1], info[2][:-1], info[3][:-1], info[4][:-1]

#         StartCheck(chromeDriverPath, level, school, name, birth, pw)

#     else:
#         CreateFile()  # info.txt 파일 생성 후 종료
#         print('\n정보가 저장되었습니다. 프로그램을 다시 실행하시면 자가진단이 시작됩니다.\n')


#######----########

# program start
def Main2():
    info = UserData()

    if not path.exists('./info.json'):  # info.json 파일 존재하지 않을 때
        info.init()
        print('\ninfo.json 파일에 정보가 저장되었습니다.\n프로그램을 다시 실행하시면 자동으로 자가진단이 시작됩니다.\n')

    else:
        info.getData()

        if not path.exists(info.driverPath):  # 크롬드라이버 파일이 존재하지 않을 때
            a = input('\n크롬드라이버가 존재하지 않습니다.\n자동으로 최신버전을 다운받으시겠습니까? (y/n) : ')

            if a in 'yY':
                print('\n드라이버 설치중...')
                success, downloadPath = installDriver()
                if not success:
                    return
                
                info.modifyDriverPath(downloadPath) # 다운로드 경로 수정

            else:
                print('\n크롬드라이버를 실행파일과 같은 폴더에 설치해주세요. (https://github.com/XxCtrlZxX/SelfCheck 참고)\n')
                return

        # 자가진단 시작
        StartCheck(info)
                    
        

Main2()

os.system("pause")
os._exit(0)
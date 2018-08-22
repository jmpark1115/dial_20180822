import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import time

USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
              '(KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')


def weather(mode='죽전동'):
    if mode == '강남역':
        sido = '서울시'
        gu = '강남구'
    else:
        sido = '용인시'
        gu = '수지구'

    search = '날씨'

    sido = urllib.parse.quote(sido)
    gu = urllib.parse.quote(gu)
    search = urllib.parse.quote(search)

    url = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%s+%s+%s' % (sido, gu, search)

    headers = {'referer': '',
               'User-Agent': 'Mozilla/5.0',
               'Accept-Language': 'ko-kr, en-us'}

    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read()

    # res = requests.get(url, headers = headers)
    # html = res.text
    soup = BeautifulSoup(html, 'lxml')

    # 오늘 날씨
    t1 = soup.find('p', {'class': 'info_temperature'}).get_text().strip()

    liList = soup.find('ul', {'class': 'info_list'}).find_all('li')
    t2 = liList[0].get_text().strip()
    t3 = liList[1].get_text().strip()
    t4 = liList[2].get_text().strip()

    dtList = soup.find('dl', {'class': 'indicator'}).find_all('dt')
    ddList = soup.find('dl', {'class': 'indicator'}).find_all('dd')

    t5 = dtList[0].get_text().strip() + ddList[0].get_text().strip()
    t6 = dtList[1].get_text().strip() + ddList[1].get_text().strip()
    t7 = dtList[2].get_text().strip() + ddList[2].get_text().strip()

    # 내일 날씨
    tomorrow = soup.find('div', {'class': 'tomorrow_area'})

    tm1 = tomorrow.find('p', {'class': 'info_temperature'}).get_text().strip()

    liList = tomorrow.find('ul', {'class': 'info_list'}).find_all('li')
    tm2 = liList[0].get_text().strip()
    tm3 = liList[1].get_text().strip()

    # 메세지 발송
    sendTiem = time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))

    # msg = "< {} {} 날씨 > \n" .format(sido.decode('utf-8'), gu.decode('utf-8'))
    msg = "[" + sendTiem + "]" + "\n" + t1 + "\n" + t2 + "\n" + t3 + "\n" + t4 + "\n" + t5 + "\n" + t6 + "\n" + t7
    msg += "\n\n" + "[내일날씨]" + "\n" + tm1 + "\n" + tm2 + "\n" + tm3

    # chat_id = '471664025'
    # chat_token = '660595227:AAHz1Yc6ywFSRD36U6Iw8XylpzpPNsGdQ0w'
    # tg = telegram(chat_token, chat_id)
    # result = tg.message(msg)
    return msg

def 블로그_검색(query):
    url = 'https://search.naver.com/search.naver'

    params = {
        'where': 'post',
        'query': query,
    }

    headers = {
        'User-Agent': USER_AGENT,
    }

    res = requests.get(url, params=params, headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')

    post_list = []

    for tag in soup.select('.sh_blog_top'):
        title_tag = tag.select_one('.sh_blog_title')

        url = title_tag['href']
        title = title_tag.text
        desc = tag.select_one('.sh_blog_passage').text
        when = tag.select_one('.txt_inline').text

        try:
            thumb_url = tag.select_one('img')['src']
        except TypeError:
            thumb_url = None

        post_list.append({
            'title': title,
            'desc': desc,
            'thumb_url': thumb_url,
            'when': when,
            'url': url,
        })

    return post_list


def 상한가_크롤링():
    '''
    네이버 금융 - 상한가 페이지 크롤링

    https://finance.naver.com/sise/sise_upper.nhn
    '''

    print("상한가_크롤링()")
    url = 'https://finance.naver.com/sise/sise_upper.nhn'

    # 파이썬에서 동작하는 브라우저인 requests를 통해,
    # 지정 URL의 서버로 요청을 보내어 응답을 받습니다.
    res = requests.get(url)

    # 받은 응답의 문자열을 html 변수에 저장합니다.
    html = res.text

    # 파싱을 위해, 아름다운스프 객체를 생성합니다.
    soup = BeautifulSoup(html, 'html.parser')

    df_list = []
    for tag in soup.select('.box_type_l'):
        category = tag.select_one('.top_tlt').text
        row_list = []
        for tr_tag in tag.select('table tr'):
            col_text_list = [
                tag.text.strip()
                for tag in tr_tag.select('th, td')
                if tag.text.strip()]
            if col_text_list:
                row_list.append(col_text_list)
          
        df = pd.DataFrame(row_list[1:], columns=row_list[0]).set_index('N')
        df['분류'] = category
        df_list.append(df)
        
    df = pd.concat(df_list)

    columns = ['분류', '종목명', '현재가', '등락률', '거래량']
    return df[columns].to_string()


def 테마별_시세_크롤링():
    print("테마별_시세_크롤링()")
    url = 'https://finance.naver.com/sise/theme.nhn'

    df = pd.read_html(url, encoding='cp949')[0].iloc[3:]
    df.columns = [
        '테마명', '전일대비', '최근3일등락률(평균)',
        '전일대비등락현황 (상승)',
        '전일대비등락현황 (보합)',
        '전일대비등락현황 (하락)',
        '주도주1', '주도주2']
    df = df.set_index('테마명')

    columns = ['전일대비', '최근3일등락률(평균)', '주도주1', '주도주2']
    return df[columns].iloc[:3].to_string()

if __name__ == '__main__':
    aa = 테마별_시세_크롤링()
    print(aa)
    bb=상한가_크롤링()
    print(bb)
    # print(블로그_검색('등려군'))
    # print(weather("죽전동"))

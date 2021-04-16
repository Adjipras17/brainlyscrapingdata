from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotInteractableException
from time import sleep
from database import dbBrainly

def get_browser():
    opts = Options()
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--no-sandbox")
    driver = Chrome(executable_path='chromedriver.exe', options=opts)
    
    return driver

def check_pop_up(driver):
    pop_up_elem = '/html/body/div[2]/div/div[3]'
    driver.implicitly_wait(10)
    try:
        driver.find_element_by_xpath(pop_up_elem).click()
        print('udah di close')

    except NoSuchElementException:
        print('tidak muncul')
        pass

    except ElementNotInteractableException:
        print('tidak ada pop up')
        pass

def get_info(driver, url):
    driver.get(url)
    sleep(3)
    check_pop_up(driver)
    #mapel
    # subject_elem = '//*[@id="question-sg-layout-container"]/div[1]/div[1]/article/div/div[2]/div[1]/div/div[2]/ul/li[2]/a'
    subject_elem = '/html/body/div[5]/div/div[1]/div[2]/div[3]/div[5]/a/div[2]/div'
    subject_name = driver.find_element_by_xpath(subject_elem).text
    #soal
    text_elem = '/html/body/div[5]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div[1]'
    text = driver.find_element_by_xpath(text_elem).text
    #status
    button_style = 'span.sg-button__text'
    content = driver.find_element_by_id('question-sg-layout-container')
    span_text = content.find_element_by_css_selector(button_style).text
    
    if 'LIHAT JAWABAN' in span_text:
        status = True
    else:
        status = False

    data = {
        'url' : url,
        'subjects' : subject_name, 
        'text_soal' : text,
        'status' : status
        }

    return data

def get_subject_links(driver):
    driver.implicitly_wait(10)
    xpath_fisika = '/html/body/div[5]/div/div[1]/div[2]/div[3]/div[5]/a/div[2]/div'
    driver.find_element_by_xpath(xpath_fisika).click()
    # ambil mapel

    xpath_load = '//*[@id="loadMore"]'
    for i in range(10):
        driver.find_element_by_xpath(xpath_load).click()
        sleep(3)
        print('load ke {}'.format(i))
        i+=1
        # klik loadmore

    xpath_queue = '/html/body/div[5]/div/div[2]/div/div'
    # queue = driver.find_elements_by_xpath(xpath_queue)
    # print(len(queue))
    for q in range(50):
        driver.find_element_by_xpath(xpath_queue + '/div[{}]'.format(q+1))
        xpath_answer = '/html/body/div[5]/div/div[2]/div/div/div[{}]/div/div/div/div[2]/div[2]/button/a'.format(q+1)
        href = driver.find_element_by_xpath(xpath_answer).get_attribute('href')
        db.insert_url('fisika', href)
        sleep(3)
        print('data dimasukkan')
        # klik tombol answer

# /html/body/div[5]/div/div[2]/div/div/div[1]/div/div/div/div[2]/div[2]/button/a
# /html/body/div[5]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div[2]/button/a
# //*[@id="#qlist"]/div/div[5]
# //*[@id="#qlist"]/div/div[10]


if __name__ == '__main__':    
    db = dbBrainly()
    driver = get_browser()
    # url = 'https://id.brainly.vip/unanswered'
    # driver.get(url)
    # get_subject_links(driver)

    # driver.close()
    data = db.get_all_urls('fisika')
    for url in data:
        try:
            u = url['url']
            value = db.check_docs('info_fisika', u)
            if value is False:
                collected = get_info(driver, u)
                db.insert_info('info_fisika', collected)
                print('info inserted')
                sleep(3)
        except NoSuchElementException:
            print('url error')
            pass

 
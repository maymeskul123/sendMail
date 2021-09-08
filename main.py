from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import string
import time


def rand_10():
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))


mail_site = 'https://tempmail.plus/ru/#!'
path_to_driver = '/home/vitalik/PycharmProjects/sendMail/Web/geckodriver'


def count_let_and_num(example):
    count_let = 0
    count_num = 0
    for i in example:
        print(i, ord(i))
        if (65 <= ord(i) <= 90) or (97 <= ord(i) <= 122):
            count_let += 1
        elif 48 <= ord(i) <= 57:
            count_num += 1
    return (count_let, count_num)


def write_mail(subject, body):
    find_element = driver.find_element_by_xpath("/html/body/div[8]/div[1]/div[2]/div[2]/button/span[2]")
    find_element.click()
    find_element = driver.find_element_by_xpath("// *[ @ id = 'to']")
    subj = driver.find_element_by_xpath("//*[@id='subject']")
    text = driver.find_element_by_xpath("//*[@id='text']")
    submit = driver.find_element_by_xpath("//*[@id='submit']")
    find_element.send_keys(val + "@mailto.plus")
    sendMails[subject] = body
    subj.send_keys(subject)
    text.send_keys(body)
    submit.click()
    time.sleep(7)

def delete_previous_mails():
    inbox_mail = driver.find_element_by_class_name("inbox")
    mails_box = inbox_mail.find_elements_by_class_name("mail")
    while len(mails_box) > 1:
        mails_box[1].click()
        driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div[1]/div[1]/button[2]/span[2]").click()
        time.sleep(5)
        driver.find_element_by_xpath("//*[@id='confirm_mail']").click()
        time.sleep(5)
        inbox_mail = driver.find_element_by_class_name("inbox")
        mails_box = inbox_mail.find_elements_by_class_name("mail")

if __name__ == '__main__':
    countSender = 15
    driver = webdriver.Firefox(executable_path=path_to_driver)
    driver.get(mail_site)
    find = driver.find_element_by_xpath("//*[@id='pre_button']")
    val = 'test_999'
    find.send_keys(u'\ue009' + u'\ue003')
    find.send_keys(val)
    find.send_keys(Keys.ENTER)
    sendMails = dict()
    for i in range(0, countSender):
        write_mail(rand_10(), rand_10())
    inbox = driver.find_element_by_class_name("inbox")
    mails = inbox.find_elements_by_class_name("mail")
    if len(mails) == countSender:
        print("Count of mails is the same!")
    else:
        print("Count of mails is not same!")
    inboxMails = dict()
    for i in range(0, countSender):
        inbox = driver.find_element_by_class_name("inbox")
        mails = inbox.find_elements_by_class_name("mail")
        key = mails[i].__getattribute__('text').split('\n')[2]
        mails[i].click()
        time.sleep(5)
        value = driver.find_element_by_xpath("//div[@class='overflow-auto mb-20']").__getattribute__('text')
        print(key, value)
        inboxMails[key.encode('ascii')] = value.encode('ascii')
        driver.find_element_by_xpath("/html/body/div[8]/div[2]/div/div[1]/div[1]/button[1]/span[2]").click()
    print(sendMails)
    print(inboxMails)
    str_arr = []
    for key in inboxMails:
        result = count_let_and_num(inboxMails[key])
        str_arr.append("Received mail on theme {:s} with message: {:s}. It contains {:d} letters and {:d} numbers\n".format(key, inboxMails[key], result[0], result[1]))
    write_mail("Test answer", str_arr)
    time.sleep(7)
    delete_previous_mails()

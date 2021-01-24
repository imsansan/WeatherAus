import requests
import smtplib
from bs4 import BeautifulSoup
from email.mime.text import MIMEText
from email.header import Header
import csv
import datetime
import re
#from ml import init
#from ml import Solution
#url = "https://weather.com/weather/today/l/cbb66885b9ded7ed9ce0621f07906cb5d22359040dedaf14fb96ce5ef6a90466"# Hoboken


def getContent(city, url):
    
    # pretend to be a browser
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'
    }
    response = requests.get(url, headers= header)  
    #print(response.content.decode('utf-8'))

    # save to local file
    file_obj = open('%s.html'% (city), 'w')  # write a html file, named weather
    file_obj.write(response.content.decode('utf-8'))  # write content
    file_obj.close()  # close file
    
    
def getWeather(city):
    weather_data = {}

    # read from weather.html
    file_obj = open('%s.html'% (city), 'r')  
    html = file_obj.read()  # take all content out
    file_obj.close()  # close html

    soup = BeautifulSoup(html, 'lxml')  # initialize BeautifulSoup
    #print(soup)

    all_div = soup.find('main', id = 'MainContent')

    weather_data['date'] = all_div.find('div', class_ = 'CurrentConditions--timestamp--1SWy5').string
    weather_data['temperature'] = all_div.find('span', class_ = 'CurrentConditions--tempValue--3KcTQ').get_text()
    weather_data['phrase'] = all_div.find('div', class_ = 'CurrentConditions--phraseValue--2xXSr').string
    
    if all_div.find('h2', class_ = 'AlertHeadline--alertText--aPVO9'):
        weather_data['alertText'] = all_div.find('h2', class_ = 'AlertHeadline--alertText--aPVO9').get_text()
    else:
        weather_data['alertText'] = ""
    
    detail = all_div.find_all('div', class_ = 'WeatherDetailsListItem--wxData--23DP5')

    weather_data['high_low'] = detail[0].get_text()
    weather_data['wind'] = detail[1].get_text()
    weather_data['humidity'] = detail[2].get_text()
    weather_data['dew_point'] = detail[3].get_text()
    weather_data['pressure'] = detail[4].get_text()
    weather_data['uv_index'] = detail[5].get_text()
    weather_data['visibility'] = detail[6].get_text()
    weather_data['moon_phase'] = detail[7].get_text()
    
    return weather_data
    #print(all_div)
    
    
def sendEmail(dic):
    '''
        sender = input('From: ')
        password = input('password: ')
        smtp_server = input('SMTP_Server: ')
        '''
    
    text = " Temperature: {}\n Phrase: {}\n Wind: {}\n Humidity: {}\n Pressure: {}\n UV Index: {}\n Visibility: {}\n Moon Phase: {}\n Alert: {}\n".format(
    dic['high_low'], dic['phrase'], dic['wind'], dic['humidity'], dic['pressure'], dic['uv_index'], dic['visibility'], dic['moon_phase'], dic['alertText']) 
    #
    sender = '499302455@qq.com'
    sent_host = 'smtp.qq.com'
    sent_user = '499302455@qq.com'
    sent_pass = '***********'
    #
    receivers = ['asun5@stevens.edu']
    message = MIMEText("Weather today in Hoboken :\n{}\n".format(text),'plain','utf-8')
    #    
    message['From'] = Header('Raspberry Pi','utf-8')    
    message['To'] = Header('An Sun','utf-8')
    Subject = "Weather Today in Hoboken" 
    message['Subject'] = Header(Subject,'utf-8')   #标题
    try:
        server = smtplib.SMTP_SSL(sent_host, 465)
        print("SMTP complete")

        #server.set_debuglevel(1)
        server.login(sent_user,sent_pass)
        print("login complete")

        server.sendmail(sender,receivers[0],message.as_string())
        print("Success")
        server.quit()

    except smtplib.SMTPException:
        print("Error")
            

def writeCSV(city, data):
    path = '%s.csv' % (city)
    print(path)
    print(data)
    
    
    today = str(datetime.date.today())
    today = today.replace('-','/')
    
    data['temperature'] = re.findall('\d+', data['temperature'])
    #print(type(data['temperature'].pop()))
    data['temperature'] = format((int(data['temperature'].pop()) - 32) / 1.8, '.1f')
    
    data['wind'] = re.findall('\d+', data['wind'])
    data['wind'] = format(int(data['wind'].pop())*1.609 , '.1f')
    
    data['humidity'] = int((re.findall('\d+', data['humidity'])).pop())
    
    data['pressure'] = re.findall('\d+\.?\d*', data['pressure'])
    data['pressure'] = format(float(data['pressure'].pop())* 33.86389 , '.1f')
    
    data['high_low'] = re.findall('\d+', data['high_low'])
    high = format((int(data['high_low'][0]) - 32) / 1.8 , '.1f')
    if len(data['high_low'])> 1:
        low = format((int(data['high_low'][1]) - 32) / 1.8 , '.1f')
    else:
        low = high
    
    #print(high, low)
    
    
    
    csvFile = open(path, 'a')
    writer = csv.writer(csvFile)
    writer.writerow([today, city, low, high, data['wind'],data['wind'], data['humidity'],data['humidity'], data['pressure'], data['pressure'],5,5,data['temperature'], data['temperature'],'No','No'])
    
    csvFile.close()
    



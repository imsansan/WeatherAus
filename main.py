from ml import dataWash
from ml import Solution
from net import getContent
from net import getWeather
from net import sendEmail
from net import writeCSV



urls ={
    "Sydney": "https://weather.com/weather/today/l/98ef17e6662508c0af6d8bd04adacecde842fb533434fcd2c046730675fba371",   
    "Melbourne": "https://weather.com/weather/today/l/02d8bffb8e85d1880181a1ecd44587f82ed240d742cef8696b0fc93931d5686d"
    }


if __name__ == '__main__':
    for city, url in urls.items():
        print(city, url)
        getContent(city, url) #get all content from website and save to local
        result = getWeather(city) # data wash and return weather data
        #print(result)
        writeCSV(city, result)
        #send_email(result)# send email
        X, Y =dataWash(city, "weatherAUS.csv")
        Solution(city, X, Y)
    print('success')
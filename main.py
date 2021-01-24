from ml import dataWash
from ml import Solution
from net import getContent
from net import getWeather
from net import sendEmail
from net import writeCSV



urls ={
    "Sydney": "**************",   
    "Melbourne": "***************"
    }


if __name__ == '__main__':
    for city, url in urls.items():
        print(city, url)
        getContent(city, url) #get all content from website and save to local
        result = getWeather(city) # data wash and return weather data
        writeCSV(city, result)
        send_email(result)# send email
        X, Y =dataWash(city, "weatherAUS.csv")
        Solution(city, X, Y)
    print('success')

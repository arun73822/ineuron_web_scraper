# Import All Required Packages
from flask import Flask,render_template,request
from flask_cors import cross_origin,CORS
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as bs
import json
import logging

# Creates the logging
logging.basicConfig(filename='ineuron.log',level=logging.DEBUG,format='%(asctime)s %(levelname)s %(message)s')

app=Flask(__name__)  # Creates the object

@app.route('/',methods=['POST'])
@cross_origin()
def homepage():
    return render_template('index.html')

@app.route('/ineuron_scraping',methods=['POST'])
@cross_origin()
def course_content():
    "This function gives the courses are available in form of list"
    if request.method=='POST':
        try:
            search_string=request.form('content').replace(" ","-").title()
            ineuron_url='https://courses.ineuron.ai/category/' + search_string
            logging.info('The search url is {}'.format(ineuron_url))
            urlclient=uReq(ineuron_url)
            ineuron_page=urlclient.read()
            urlclient.close()
            logging.info('Successfully reads the page')
            ineuron_html=bs(ineuron_page,'html_parser')
            data=bs(str(ineuron_html.findAll('script',{'type':'application/json'}))).script.text
            json_file=json.loads(data)
            global course_list
            course_list=list(json_file['props']['pageProps']['initialState']['init']['courses'])
            print(course_list)
        except Exception as e:
            print("Something wrong please check {}".format(e))
            logging.info("Something wrong please check {}".format(e))

def create_url():
    " This function gives the url for each course"
    url="https://courses.ineuron.ai/"
    global courses_url_list
    course_url_list=[]
    for data in course_list:
        data.replace(" ","-")
        total_url=url + data
        courses_url_list.append(total_url)
    return course_url_list

def results():
    " This function gives the all courses details"
    courses_list=[]
    for data in courses_url_list:
        uclient=uReq(data)
        ineuron_page=uclient.read()
        uclient.close()
        ineuron_html=bs(ineuron_page,'html.parser')
        jsonfile=bs(str(ineuron_html.findAll("script",{"type":"application/json"}))).script.text
        data1=json.loads(jsonfile)
        try:
            course_name=data1['props']['pageProps']['data']['title']
        except:
            course_name= "No Name"
        try:
            JobGuaranteeProgram=data1['props']['pageProps']['data']['isJobGuaranteeProgram']
        except:
            JobGuaranteeProgram= "NO"
        try:
            on_going=data1['props']['pageProps']['data']['details']['active']
        except:
            on_going= "NONE"
        try:
            description=data1['props']['pageProps']['data']['details']['description']
        except:
            description= "There is no description"
        try:
            video_url=data1['props']['pageProps']['data']['details']['videoURL']
        except:
            video_url= "Not found"
        try:
            mode=data1['props']['pageProps']['data']['details']['mode']
        except:
            mode="None"
        try:
            price=data1['props']['pageProps']['data']['details']['pricing']['IN']
        except:
            price= "FREE"
        try:
            duration=data1['props']['pageProps']['data']['meta']['duration']
        except:
            duration= "None"
        try:
            learn=data1['props']['pageProps']['data']['meta']['overview']['learn']
        except:
            learn= "Content not available"
        try:
            requirements=data1['props']['pageProps']['data']['meta']['overview']['requirements']
        except:
            requirements= "There is no requirements present"
        try:
            features=data1['props']['pageProps']['data']['meta']['overview']['features']
        except:
            features= "Features are not available"

        mydict={'coursename':course_name,'JobGuaranteeProgram':JobGuaranteeProgram,'ongoing':on_going,
                'description':description,'video_url':video_url,'mode':mode,'price':price,
                'duration':duration,'learn':learn,'requirements':requirements,'features':features
        }
        courses_list.append(mydict)
    return render_template('results.html', result=courses_list[0:(len(courses_list)-1)])
        
if __name__=='__main__':
    app.run(debug=True)
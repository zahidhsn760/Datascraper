from flask import Flask, request, render_template,json,redirect, jsonify
import mysql.connector
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app =Flask(__name__)
@app.route('/', methods=['GET'])
def search():
    return render_template('index.html')


       
 # Connect to the database
def database(name, DoB, life, address, phonenum):
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='scraping data')
    name1= name
    DoB1=DoB
    life1=life
    address1=address
    Phonenum1 = phonenum
    cursor = conn.cursor()
    try:
                query="INSERT INTO scrapy1(Phone_Number, Name, Date_of_Birth, Life_Status, Residence) VALUES (%s, %s, %s,%s,%s)"
                query1="ON CONFLICT (Phone_Number) DO NOTHING;"
                # cursor.execute(query,(Phonenum, name1,DoB1,life1,address1))
                # Check if the customer already exists in the table
                cursor.execute("SELECT COUNT(*) FROM scrapy1 WHERE Phone_Number = %s", ('555-555-5555',))
                result = cursor.fetchone()

                if result[0] == 0:
                    cursor.execute(query,(Phonenum1, name1,DoB1,life1,address1))
                conn.commit()
                print("Record inserted.")
    except  mysql.connector.errors.IntegrityError as e:
                    if e.msg.startswith("Duplicate entry"):
                     print(f"Record for {Phonenum1} already exists.")
                    else:
                     print("An error occurred:", e)

    finally:
             cursor.close()
             conn.close()
@app.route('/submit', methods=['POST'])
def Scraping():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
     text = request.form['search_bar']
     options = Options()
     options.page_load_strategy = 'normal'
    # options.add_argument("--disable-javascript")  # Disable JavaScript
    #  options.add_argument("--headless")  # Run in headless mode
    # options.add_argument("--no-sandbox")  # Bypass OS security model
    # options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    # options.add_argument("start-maximized")  # open Browser in maximized mode
    # options.add_argument("disable-infobars")  # disabling infobars
    # options.add_argument("--disable-extensions") # disabling extensions
    # options.add_argument("--disable-gpu")  # applicable to windows os only
    # options.add_argument("--remote-debugging-port=9222")  #use this port to debug
    # options.add_argument("--disable-browser-side-navigation")  # Disable browser side navigation
    # options.add_argument("--disable-features=VizDisplayCompositor") # Disable 



     browser = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options)

    # navigate to a website
     browser.get('http://411find.com/reverse-phone')
     search =browser.find_element(By.CLASS_NAME, "form-inline")
     folder = browser.find_element(By.ID, 'phonenum')
     Phonenum=text
     folder.send_keys(Phonenum)
     search_bar =browser.find_element(By.TAG_NAME, "button")





    
     search_bar.click()
     time.sleep(5)

     url = f'http://411find.com/reverse-phone/Phonenum={Phonenum}'
     details =browser.find_elements(By.CLASS_NAME,"details")
     if details != []:
        index = browser.find_elements(By.TAG_NAME,"li")
        zx=index[4].text
        y= zx.split('\n')
        print(y)
        name=y[0].split(':')
        name=name[1]
        DoB=y[1].split(':')
        DoB=DoB[1]
        life=y[2].split(':')
        life=life[1]
        
        if len(y)< 5 :
           address = None
          #  database(name, DoB, life, address,Phonenum) 
           def write_json(data, filename='templates//new_json.json'):
                # text = request.form['search_bar']
                # name, DoB, life, address, Phonenum=Scraping(data)
                with open(filename,"w")as f:
                    json.dump(data,f,indent=1)
                     
            
           data = {
                'Status': 'success',
                  'phone_number':Phonenum,
                  'name': name,
                   'date_of_birth': DoB,
                   'life_status':life,
                   'residence': address
        
                     }
            
          
           write_json(data)
           

        else:
          address=y[4]
          # database(name, DoB, life, address, Phonenum)
          def write_json(data, filename='templates//new_json.json'):
                # text = request.form['search_bar']
                # name, DoB, life, address, Phonenum=Scraping(text,data)
                with open(filename,"w")as f:
                    json.dump(data,f,indent=1)
                     
            
          data = {
                  'Status': 'success',
                  'phone_number':Phonenum,
                  'name': name,
                   'date_of_birth': DoB,
                   'life_status':life,
                   'residence': address

        
                     }
          
            
          write_json(data)
        return render_template('new_json.json')

     else:       
        return jsonify({"Status":"warning","StatusMessage":"Noting Found"}),404  
if __name__=='__main__':
# Scraping()
 app.run(debug=True)
from flask import Flask, jsonify
import json
from datetime import datetime
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Initialize WebDriver globally
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-software-rasterizer")
chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10.0)
driver.get('https://elevennorth.com/floorplans/')

@app.route('/')
def lambda_handler():
    try:
        # Wait for and click on floor 1
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.skylease__toolbar-floor-link:nth-child(1)"))
        )
        driver.execute_script("arguments[0].click();", element)
        
        # FLOOR 1 - Parse and collect data
        records1 = pd.DataFrame(driver.find_element(By.CSS_SELECTOR, "#unit-list").text.split(), columns=['record'])
        init_df1 = pd.DataFrame(np.array(records1['record']).reshape(-1,11))
        init_df1.columns = ['unit_number', 'beds', 'c', 'bath', 'e', 'sq_ft', 'g', 'h', 'i', 'j', 'starting_at']
        floor1 = init_df1.loc[:, ('unit_number', 'beds', 'bath', 'sq_ft', 'starting_at')]
        floor1['property'] = driver.title

        # Wait for and click on floor 2
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.skylease__toolbar-floor-link:nth-child(1)"))
        )
        driver.execute_script("arguments[0].click();", element)
        
        # FLOOR 2 - Parse and collect data
        records2 = pd.DataFrame(driver.find_element(By.CSS_SELECTOR, "#unit-list").text.split(), columns=['record'])
        init_df2 = pd.DataFrame(np.array(records2['record']).reshape(-1,11))
        init_df2.columns = ['unit_number', 'beds', 'c', 'bath', 'e', 'sq_ft', 'g', 'h', 'i', 'j', 'starting_at']
        floor2 = init_df2.loc[:, ('unit_number', 'beds', 'bath', 'sq_ft', 'starting_at')]
        floor2['property'] = driver.title

        # Wait for and click on floor 3
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.skylease__toolbar-floor-link:nth-child(1)"))
        )
        driver.execute_script("arguments[0].click();", element)
        
        # FLOOR 3 - Parse and collect data
        records3 = pd.DataFrame(driver.find_element(By.CSS_SELECTOR, "#unit-list").text.split(), columns=['record'])
        init_df3 = pd.DataFrame(np.array(records3['record']).reshape(-1,11))
        init_df3.columns = ['unit_number', 'beds', 'c', 'bath', 'e', 'sq_ft', 'g', 'h', 'i', 'j', 'starting_at']
        floor3 = init_df3.loc[:, ('unit_number', 'beds', 'bath', 'sq_ft', 'starting_at')]
        floor3['property'] = driver.title


        # Wait for and click on floor 4
        element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.skylease__toolbar-floor-link:nth-child(1)"))
        )
        driver.execute_script("arguments[0].click();", element)
        
        # FLOOR 4 - Parse and collect data
        records4 = pd.DataFrame(driver.find_element(By.CSS_SELECTOR, "#unit-list").text.split(), columns=['record'])
        init_df4 = pd.DataFrame(np.array(records4['record']).reshape(-1,11))
        init_df4.columns = ['unit_number', 'beds', 'c', 'bath', 'e', 'sq_ft', 'g', 'h', 'i', 'j', 'starting_at']
        floor4 = init_df4.loc[:, ('unit_number', 'beds', 'bath', 'sq_ft', 'starting_at')]
        floor4['property'] = driver.title

        result = pd.concat([floor1, floor2,floor3,floor4])
        now = datetime.now()
        date_time = now.strftime("%m-%d-%Y_%H-%M-%S")
        result['pulled_at'] = date_time

        result_json = result.to_dict(orient='records')

        return jsonify({
            'statusCode': 200,
            'body': result_json
        })

    except Exception as e:
        return jsonify({
            'statusCode': 500,
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
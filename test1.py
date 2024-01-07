from bs4 import BeautifulSoup
import requests
import time
import pandas as pd

def get_aruba_dashboard_cookie(url, account, password):
    '''
    get_aruba_dashboard_cookie: Returns the cookie of an ARUBA Dashboard
        Parameters:
            - url       : URL of Aruba dashboard login website
            - account   : User account
            - password  : User password
    '''
    aruba_dashboard_cookie = ''
    params = {
        'dashboard_url': url + '/screens/wms/wms.login',
        'payload': 'opcode=login&url=%2Flogin.html&needxml=0&uid=' + account +'&passwd='+ password,
        'headers': {'Content-Type': 'text/html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }
    }

    get_aruba_login_data = requests.post(params['dashboard_url'],
                                  data=params['payload'].encode('utf-8'),
                                  headers=params['headers'],
                                  verify=False
                                  )

    status_code = get_aruba_login_data.status_code

    if status_code != 200:
        print("Error Status Code: ", status_code)
    else:
        aruba_dashboard_cookie = get_aruba_login_data.cookies['SESSION']
        print("Successfully Retrieved Aruba Cookie")
    return aruba_dashboard_cookie

def parse_aruba_data_to_dataframe(aruba_raw_data):
    '''
    parse_aruba_data_to_dataframe: Parse the AP or Client data to DataFrame format 
        Parameters:
            - aruba_raw_data     : AP or Client raw data from aruba dashboard
    '''
    # Parse AP data
    parsed_raw_data = BeautifulSoup(aruba_raw_data.text, 'html.parser')
    parameter_name = parsed_raw_data.find_all('header')
    parameter_value = parsed_raw_data.find_all('row')
    
    """
    DataFrame format
    """
    
    aruba_data = pd.DataFrame() 
    index = 0
    
    # Parameter value
    for values in parameter_value:
        
        parameter_value_total = []
        parameter_value = values.find_all('value')
        
        time_stamp = int(time.time())
        struct_time = time.localtime(time_stamp)
        timeString = time.strftime("%Y-%m-%d-%H-%M", struct_time)
        parameter_value_total.append(time_stamp)

        for i in range(len(parameter_value)):
            parameter_value_total.append(parameter_value[i].text)

        index += 1
        aruba_data[index] = parameter_value_total
    
    # Parameter name
    for name in parameter_name:
        
        parameter_name_total = []
        parameter_name_total.append('time_stamp')
        parameter_name = name.find_all('column_name')
        
        for i in range(len(parameter_name)):
            parameter_name_total.append(parameter_name[i].text)


    aruba_data.index = parameter_name_total
    aruba_data = aruba_data.T
    aruba_data.reset_index(drop=True, inplace=True)

def get_aruba_ap_data(url, cookie):
    '''
    get_aruba_ap_data: Returns all of AP data in Aruba controller 
        Parameters:
            - url       : URL of Aruba dashboard website
            - account   : User account
    '''
    payload_parameter = 'ap_name radio_band total_data_bytes rx_data_bytes channel_str radio_mode eirp_10x max_eirp noise_floor arm_ch_qual sta_count current_channel_utilization rx_time tx_time channel_interference channel_free channel_busy avg_data_rate tx_avg_data_rate rx_avg_data_rate ap_quality'
    params = {
        'dashboard_url': url + '/screens/cmnutil/execUiQuery.xml',
        'payload': 'query=<aruba_queries><query><qname>backend-observer-radio-28</qname><type>list</type><list_query><device_type>radio</device_type><requested_columns>' + payload_parameter +'</requested_columns><sort_by_field>ap_name</sort_by_field><sort_order>asc</sort_order><pagination><start_row>0</start_row><num_rows>400</num_rows></pagination></list_query></query></aruba_queries>&UIDARUBA=' + cookie,
        'dashboard_cookie' : {"SESSION": cookie},
        'headers': {'Content-Type': 'text/plain'}
    }

    aruba_ap_raw_data = requests.post(params['dashboard_url'],
                                  data=params['payload'].encode('utf-8'),
                                  cookies=params['dashboard_cookie'],
                                  headers=params['headers'],
                                 verify=False
                                  )

    status_code = aruba_ap_raw_data.status_code

    if status_code != 200:
        print("Error Status Code: ", status_code)
    else:
        print("Successfully Retrieved the raw data of Aruba APs")
    
    aruba_ap_data = parse_aruba_data_to_dataframe(aruba_ap_raw_data)
        
    return aruba_ap_data

if __name__ == '__main__':
    cookie = get_aruba_dashboard_cookie("","","")
    print(cookie)
    ap_data = get_aruba_ap_data("",cookie)
    print(ap_data)

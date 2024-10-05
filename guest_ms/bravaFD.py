"""
>> TASK:

A SOFTWARE THAT PERFORMS MAJOR FRONT OFFICE OPERATIONS (CHECK-IN, CHECK-OUT, ROOM-TRANSFER, BILLING, RESERVATION, PAYMENT POSTING,
GUEST HISTORY AND UTILITY MONITOR).

>> APPROACH:
1. CREATE A CLASS THAT CONTAINS ALL FUNCTIONS FOR EACH FRONT OFFICE PROCEDURE SUCH THAT THE CHECK-IN PROCEDURE HAS ITS OWN FUNCTION WITHIN
    THE CLASS.

2. THE FUNCTIONS IN THE CLASS INITIATES A CONNECTION WITH THE MYSQL DATABASE FOR STORAGE, MANIPULATION AND INFORMATION RETRIEVAL, DEPENDING
    ON THE PROCEDURE INITIATED.

3. THE SOFTWARE LOADS A STREAMLIT APP ON LOCAL HOST WITH CONTAINING DIFFERENT SEGMENTS, TAILORED FOR DIFFERENT PROCEDURES.
"""

import streamlit as st
import mysql.connector, pandas as pd
from datetime import datetime, timedelta
from time import sleep
from streamlit_dynamic_filters import DynamicFilters

def greet():
    time = datetime.now().strftime("%H:%M:%S")
    hour = time.split(":")[0]
    if hour >= '00' and hour <= '11':
        return ('GOOD MORNING! 🌇')
    elif hour >= '12' and hour < '16':
        return('GOOD AFTERNOON! 🌞')
    else:
        return ('GOOD EVENING! 🌆')
    return

def intro():
    st.title('👨‍💼')
    st.header(f"""
                {greet()}\n
                * THIS IS THE BRAVA HOTEL'S GUEST MANAGEMENT SOFTWARE. \n
                * PLEASE ENSURE THAT YOU HAVE BEEN GIVEN ORIENTATION AS REGARDS THIS SOFTWARE.\n
                * IF NOT, KINDLY SEE YOUR SUPERVISOR OR I.T.\n
                * IF YOU ARE UNFAMILIAR WITH A PARTICULAR STEP, DO NOT GO FURTHER! PAUSE AND INFORM YOUR SUPERVISOR OR I.T.!\n
                * REMEMBER TO SMILE!
                * SEE THE ARROW UP THERE? CLICK IT TO EXPAND AND SEE AVAILABLE OPTIONS.
                * GOOD LUCK.
            """)

class MYSQL_CONNECT:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            **st.secrets['connection']
        )
    
        cursor = self.mydb.cursor()
        cursor.execute("""CREATE DATABASE IF NOT EXISTS BRAVA_HOTEL""")
        cursor.execute("""USE BRAVA_HOTEL""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS HISTORY (
                       ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       GUEST_NAME VARCHAR(200) NOT NULL,
                       RECEPTIONIST VARCHAR(50) NOT NULL,
                       ADDRESS TEXT DEFAULT NULL,
                       CITY VARCHAR(50) DEFAULT NULL,
                       STATE VARCHAR(50) DEFAULT NULL,
                       POSTAL_CODE VARCHAR(50) DEFAULT NULL,
                       COUNTRY VARCHAR(50) DEFAULT NULL,
                       PHONE_NUMBER VARCHAR(50) NOT NULL,
                       EMAIL_ADDRESS VARCHAR(50) DEFAULT NULL,
                       NATIONALITY VARCHAR(50) DEFAULT NULL,
                       AMOUNT_OF_GUESTS INT(10) NOT NULL DEFAULT '1',
                       ID_NUMBER VARCHAR(50) DEFAULT NULL,
                       ID_MEANS VARCHAR(50) NOT NULL,
                       ARRIVAL_DATE DATE,
                       ARRIVAL_TIME TIME NOT NULL,
                       NO_OF_NIGHTS SMALLINT NOT NULL DEFAULT '1',
                       ROOM_NUMBER VARCHAR(20) NOT NULL,
                       EXPECTED_DEPARTURE DATE,
                       ACTUAL_DEPARTURE DATE,
                       SPECIAL_REQUESTS SET('NON SMOKING ROOM', 'EXTRA PILLOWS', 'BABY CRIB', 'LATE CHECK OUT', 'CAR PARK VIEW') DEFAULT NULL,
                       OTHER_SPECIAL_REQUESTS TEXT DEFAULT NULL,
                       ROOM_RATE MEDIUMINT UNSIGNED NOT NULL,
                       DISCOUNTED_RATE VARCHAR(50) NOT NULL,
                       DEPOSIT BIGINT UNSIGNED NOT NULL,
                       CHARGES INT UNSIGNED NOT NULL,
                       BALANCE BIGINT SIGNED NOT NULL DEFAULT '0');""")

    def mysql_create_connect_checkin(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f'USE {db}')
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}
                       ( ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       GUEST_NAME VARCHAR(200) NOT NULL,
                       RECEPTIONIST VARCHAR(50) NOT NULL,
                       ADDRESS TEXT DEFAULT NULL,
                       CITY VARCHAR(50) DEFAULT NULL,
                       STATE VARCHAR(50) DEFAULT NULL,
                       POSTAL_CODE VARCHAR(50) DEFAULT NULL,
                       COUNTRY VARCHAR(50) DEFAULT NULL,
                       PHONE_NUMBER VARCHAR(50) NOT NULL,
                       EMAIL_ADDRESS VARCHAR(50) DEFAULT NULL,
                       NATIONALITY VARCHAR(50) DEFAULT NULL,
                       AMOUNT_OF_GUESTS INT(10) NOT NULL DEFAULT '1',
                       ID_NUMBER VARCHAR(50) DEFAULT NULL,
                       ID_MEANS VARCHAR(50) NOT NULL,
                       ARRIVAL_DATE DATE,
                       ARRIVAL_TIME TIME NOT NULL,
                       NO_OF_NIGHTS SMALLINT NOT NULL DEFAULT '1',
                       ROOM_NUMBER VARCHAR(20) NOT NULL,
                       EXPECTED_DEPARTURE DATE,
                       SPECIAL_REQUESTS SET('NON SMOKING ROOM', 'EXTRA PILLOWS', 'BABY CRIB', 'LATE CHECK OUT', 'CAR PARK VIEW') DEFAULT NULL,
                       OTHER_SPECIAL_REQUESTS TEXT DEFAULT NULL,
                       ROOM_RATE MEDIUMINT UNSIGNED NOT NULL,
                       DISCOUNTED_RATE VARCHAR(50) NOT NULL)""")
            
    def mysql_create_connect_power_start(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db}')
        cursor.execute(f'USE {db}')
        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table}
                        (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        UTILITY VARCHAR(50) NOT NULL,
                        START_TIME TIME,
                        START_DATE_TIME TIMESTAMP)""")
        return
    
    def mysql_create_connect_power_stop(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db}')
        cursor.execute(f'USE {db}')
        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table}
                        (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        UTILITY VARCHAR(50) NOT NULL,
                        STOP_TIME TIME,
                        STOP_DATE_TIME TIMESTAMP)""")
        return
    
    def transaction(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        cursor.execute(f"USE {db}")
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS {table}
                       (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       ROOM_NUMBER INT NOT NULL,
                       ID_NUMBER VARCHAR(10) DEFAULT NULL,
                       DESCRIPTION VARCHAR(50) NOT NULL,
                       CHARGES INT NOT NULL DEFAULT '0',
                       CREDITS INT NOT NULL DEFAULT '0',
                       METHOD_OF_PAYMENT SET('TRANSFER', 'POS', 'CASH', 'VOUCHER', 'COMPLEMENTARY') NOT NULL DEFAULT 'TRANSFER',
                       COMMENT TEXT DEFAULT NULL,
                       DATE DATETIME
                       )""")
        return

    def transfers(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        cursor.execute(f"USE {db}")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}
                       (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       FORMER_ROOM INT NOT NULL,
                       DETAILS SET('WATER-HEATER', 'AIR-CON', 'INTERNET', 'T/V', 'OTHER') DEFAULT 'OTHER',
                       NEW_ROOM INT NOT NULL,
                       DATE_TIME TIMESTAMP)""")
        
    def reservation(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        cursor.execute(f"USE {db}")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}
                       (ID INT PRIMARY KEY AUTO_INCREMENT,
                       GUEST_NAME VARCHAR(50) NOT NULL,
                       CONTACT_INFO VARCHAR(50) DEFAULT NULL,
                       ARRIVAL_DATE DATE,
                       DURATION MEDIUMINT NOT NULL DEFAULT '1',
                       ROOM_CATEGORY VARCHAR(50) NOT NULL,
                       PAX MEDIUMINT NOT NULL DEFAULT "1",
                       RATE MEDIUMINT NOT NULL DEFAULT '0',
                       DEPOSIT MEDIUMINT NOT NULL DEFAULT '0',
                       BALANCE MEDIUMINT NOT NULL DEFAULT '0',
                       REQUEST TEXT DEFAULT NULL,
                       COMMENT TEXT)
                       """)

def guest_check_in():
    st.header(f"""{greet()}""")
    with st.form(key = 'NEW_FORM', clear_on_submit = True, border = True):
        st.title("""BRAVA HOTEL GUEST REGISTRATION FORM 📃 🖋️""")
        st.write('THE SECTIONS MARKED ** ARE COMPULSORY!')
        col1, col2, col3 = st.columns(3)
        guest_name = col1.text_input(label = 'GUEST NAME**')
        with col3.popover('FRONT DESK STAFF **'):
            st.markdown('Receptionist on duty')
            fd_name = st.text_input('INPUT YOUR NAME HERE (AS YOU HAVE ON YOUR NAME TAG!!)')

        col1, col2 = st.columns(2)
        guest_address = col1.text_input(label = 'GUEST ADDRESS')
        amt_of_guests = col2.slider(label = 'HOW MANY GUESTS IN A ROOM?', min_value=1, max_value=5, step = 1, value=1)

        col1, col2, col3 = st.columns(3)
        city = col1.text_input(label = 'CITY', value = 'IBADAN')
        state = col2.text_input(label = 'STATE', value = 'OYO')
        postal_code = col3.text_input(label = 'POSTAL CODE')

        col1, col2, col3 = st.columns(3)
        country = col1.text_input(label = 'COUNTRY **', value = 'NIGERIA')
        phone_no = col2.text_input(label = 'PHONE NUMBER **')
        email = col3.text_input(label = 'EMAIL')
        
        col1, col2, col3 = st.columns(3)
        nationality = col1.text_input(label = 'NATIONALITY', value = 'NIGERIAN')
        with col2.popover(label = 'MEANS OF IDENTIFICATION **'):
            id_means = st.radio('MEANS OF IDENTIFICATION', ['NATIONAL ID', 'INTERNATIONAL PASSPORT', 'DRIVERS LICENCE', 'STUDENT ID'])
        identification = col3.text_input(label = 'ID_NUMBER **')

        col1, col2, col3 = st.columns(3)
        arr_date = col1.date_input(label='ARRIVAL DATE **')

        time_of_arrival = datetime.now()
        arr_time = time_of_arrival.strftime("%H:%M:%S")
        
        no_of_nights = col2.number_input(label = 'NUMBER OF NIGHTS **', min_value=1, max_value=30, step=1)
        room_number = col3.text_input(label = 'ROOM NUMBER **')
        if arr_time.split(':')[0] >= '00' and arr_time.split(':')[0] <= '03':
            arr_date = arr_date - timedelta(days=1)
        else:
            arr_date = arr_date
            
        expected_departure = arr_date + timedelta(days=no_of_nights)

        special_requests = [
            'NON SMOKING ROOM',
            'EXTRA PILLOWS',
            'BABY CRIB',
            'LATE CHECK OUT',
            'CAR PARK VIEW'
        ]

        col1, col2 = st.columns(2)
        requests = ','.join(col1.multiselect(label = 'SPECIAL REQUESTS', options = special_requests))
        other_req = col2.text_area(label = 'OTHER REQUESTS')

        col1, col2, col3, col4  = st.columns(4)
        rack_rate = col1.text_input(label = 'RACK RATE **', help= "This is the actual rate of the room!")
        discounted_rate = col2.text_input(label = 'DISCOUNTED RATE **', value='0', help='In case of complementary guests, leave value at zero!')

        submit_form = st.form_submit_button('REGISTER')
        
        if submit_form:
            try:
                new_sql = MYSQL_CONNECT()
                new_sql.mysql_create_connect_checkin(
                    db = 'BRAVA_HOTEL',
                    table = 'IN_HOUSE'
                )
                cursor = new_sql.mydb.cursor()
                cursor.execute("""
                               SELECT ROOM_NUMBER FROM IN_HOUSE;
                               """)
                result = cursor.fetchall()
                
                from functools import reduce
                room_check = []
                for i in result:
                    i = str(i)
                    i = [x for x in i if x not in ["(", ")", ",", "'", "'"]]
                    i = reduce(lambda a, b: a+b, i)
                    room_check.append(i)

                if (not guest_name or not country or not phone_no or not identification):
                    st.warning('Make sure you fill all asterisked parts!!!')
                    st.stop()
                elif (not arr_date or not no_of_nights or not fd_name or not id_means):
                    st.warning('Make sure you fill all asterisked sections!!!')
                    st.stop()
                elif (not room_number or not rack_rate or not discounted_rate):
                    st.warning('Make sure you fill all asterisked sections!!!')
                    st.stop()
                elif (room_number in room_check):
                    st.warning('ROOM HAS NOT BEEN CHECKED OUT!!!')
                    st.stop()
                else:
                    # Sending the registered guest to the hotel's history.
                    st.success("Records have been saved successfully.", icon='✅')

                    check_in_query = """INSERT INTO IN_HOUSE
                    (GUEST_NAME, RECEPTIONIST, ADDRESS,
                    CITY, STATE, POSTAL_CODE, COUNTRY, 
                    PHONE_NUMBER, EMAIL_ADDRESS, NATIONALITY, 
                    AMOUNT_OF_GUESTS, ID_NUMBER, ID_MEANS, 
                    ARRIVAL_DATE, ARRIVAL_TIME, NO_OF_NIGHTS, 
                    ROOM_NUMBER, EXPECTED_DEPARTURE, SPECIAL_REQUESTS, 
                    OTHER_SPECIAL_REQUESTS, ROOM_RATE, DISCOUNTED_RATE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    value = (guest_name, fd_name, guest_address,
                                city, state, postal_code, country,
                                phone_no, email, nationality,
                                amt_of_guests, identification, id_means,
                                arr_date, arr_time, no_of_nights, room_number,
                                expected_departure, requests, other_req, rack_rate,
                                discounted_rate)
                    
                    cursor.execute(check_in_query, value)
                    new_sql.mydb.commit()
            except:
                with st.snow():
                    sleep(2)
                st.warning("THERE IS SOMETHING WRONG SOMEWHERE. PLEASE CONTACT YOUR SOFTWARE ADMINISTRATOR...")

    st.divider()
    with st.expander('SEE IN_HOUSE GUESTS HERE: ', expanded = False):
        in_house = MYSQL_CONNECT()
        in_house.mysql_create_connect_checkin(
                    db = 'BRAVA_HOTEL',
                    table = 'IN_HOUSE'
                )
        
        st.subheader('IN HOUSE GUESTS')
        query = f'SELECT GUEST_NAME, ARRIVAL_DATE, ROOM_NUMBER FROM IN_HOUSE;'
        df = pd.read_sql(query, in_house.mydb)
        df['ROOM_NUMBER'] = df['ROOM_NUMBER'].astype('int')
        st.write(df)
        num1, num2, num3, num4 = st.columns(4)
        print_in = num1.button(label='PRINT')
        if print_in:
            try:
                from pathlib import Path
                import os
                import openpyxl
                from openpyxl.styles import Font
                from openpyxl import load_workbook
                import time
                file = Path(Path.cwd().parent/'room_list.xlsx')
                df.to_excel(file)
                workbook = load_workbook(filename=file)
                sheet = workbook.active
                sheet.insert_rows(idx = 1, amount=2)
                sheet['A3'] = 'S/N'
                sheet.column_dimensions['B'].width = 30
                sheet.column_dimensions['C'].width = 15
                sheet.column_dimensions['D'].width = 20
                sheet['B1'] = 'BRAVA HOTEL'
                sheet['B2'] = 'IN HOUSE GUEST'
                sheet['A3'].font = Font(bold = True)
                sheet['B1'].font = Font(bold = True)
                sheet['B2'].font = Font(bold = True)
                workbook.save(file)
                os.startfile(file, 'print')
                time.sleep(9)
                os.remove(file)
            except:
                st.warning("No active printer detected!!!")

    return

def guest_checkout():
    try:
        chekoutsql = MYSQL_CONNECT()
        cursor = chekoutsql.mydb.cursor()
        cursor.execute("""USE BRAVA_HOTEL""")
        cursor.execute("SELECT ROOM_NUMBER FROM IN_HOUSE")
        result = cursor.fetchall()

        from functools import reduce
        room_number = []
        for i in result:
            i = str(i)
            i = [x for x in i if x not in ["(", ")", ",", "'", "'"]]
            i = reduce(lambda a, b: a+b, i)
            room_number.append(i)
        
        with st.popover("CHOOSE ROOM HERE"):
            room_number = st.radio("PICK A ROOM TO CHECK OUT HERE:", options=room_number)

        st.subheader("DETAILS OF CHECKOUT ROOM")
        query = f"SELECT GUEST_NAME, PHONE_NUMBER, AMOUNT_OF_GUESTS, ARRIVAL_DATE, EXPECTED_DEPARTURE, ROOM_NUMBER, ROOM_RATE, DISCOUNTED_RATE FROM IN_HOUSE WHERE ROOM_NUMBER = {room_number}"
        df = pd.read_sql(query, chekoutsql.mydb)
        df['DISCOUNTED_RATE'] = df['DISCOUNTED_RATE'].astype(int)
        st.dataframe(df)

        name, phone_number, arrival_date, expected_dep, room_no, room_rate, discounted_rate = (df.at[0, 'GUEST_NAME'],
                                                                                        df.at[0, 'PHONE_NUMBER'],
                                                                                        df.at[0, 'ARRIVAL_DATE'],
                                                                                        df.at[0, 'EXPECTED_DEPARTURE'],
                                                                                        df.at[0, 'ROOM_NUMBER'],
                                                                                        df.at[0, 'ROOM_RATE'],
                                                                                        df.at[0, 'DISCOUNTED_RATE'])
        arrival_date_new = str(arrival_date)
        arrival_date_new = datetime.strptime(arrival_date_new, "%Y-%m-%d")
        check_out_day = datetime.now().strftime("%Y-%m-%d")
        check_out_day_new = datetime.strptime(check_out_day, "%Y-%m-%d")
        day_diff = (check_out_day_new - arrival_date_new).days
        deposit = 0
        balance = deposit - (discounted_rate*day_diff)

        with st.expander('SEE GUEST INFO HERE:'):
            col1, col2, col3 = st.columns(3)
            col1.metric(label='GUEST NAME', value = name)
            col2.metric(label="ROOM NUMBER", value=room_no)
            col3.metric(label="PHONE NUMBER", value = phone_number)

            col1, col2, col3 = st.columns(3)
            col1.metric(label="ARRIVAL DATE", value = str(arrival_date))
            col2.metric(label = "EXPECTED DEPARTURE DATE", value=str(expected_dep))
            col3.metric(label="ACTUAL DEPARTURE DATE", value=check_out_day)

            col1, col2, col3 = st.columns(3)
            col1.metric(label="RACK RATE (NGN)", value=room_rate)
            col2.metric(label="DISCOUNTED RATE (NGN)", value = discounted_rate)
            col3.metric(label="DEPOSIT (NGN)", value=deposit)

            st.metric(label="BALANCE (NGN)", value=balance)

        check_out = st.button("CHECK OUT")
        if check_out:
            cursor.execute(f"DELETE FROM IN_HOUSE WHERE ROOM_NUMBER = {room_number}")
            chekoutsql.mydb.commit()
            st.info(f"SUCCESSFULLY CHECKED OUT ROOM {room_number}")
            st.rerun(scope='fragment')
    except:
        st.warning('THERE IS NO ROOM TO CHECK OUT YET...')

def posting():
    try:
        billsql=MYSQL_CONNECT()
        billsql.transaction(
            db='BRAVA_HOTEL',
            table='TRANSACTION'
        )
        cursor = billsql.mydb.cursor()
        cursor.execute("USE BRAVA_HOTEL")
        cursor.execute("SELECT ROOM_NUMBER FROM IN_HOUSE")
        result = cursor.fetchall()

        from functools import reduce
        room_number = []
        for i in result:
            i = str(i)
            i = [x for x in i if x not in ["(", ")", ",", "'", "'"]]
            i = reduce(lambda a, b: a+b, i)
            room_number.append(i)

        post =[
            'LAUNDRY',
            'CAR-WASH',
            'ROOM-CHARGES',
            'SWIMMING POOL',
            'BAR',
            'RESTAURANT',
            'PHOTOSHOOT'
        ]

        with st.form(key='BILLING', clear_on_submit=True, border=True):
            st.header("IN-HOUSE GUESTS TRANSACTIONS ARE POSTED HERE")
            st.write("THE SECTIONS WITH DOUBLE ASTERICKS ARE COMPULSORY!!")
            
            col1, col2, col3 = st.columns(3)
            with col1.popover("SELECT ROOM TO POST BILL **:"):
                room = st.radio("SELECT ROOM HERE", options=room_number)

            bill_no = col2.text_input(label='ENTER DOCKET NUMBER HERE:')

            with col3.popover("CHOOSE THE POSTING DEPARTMENT:"):
                description = st.radio(label='SELECT THE POST DEPARTMENT HERE: **', options=post)
            
            col1, col2 = st.columns(2)
            charges = col1.text_input(label='CHARGE AMOUNT **')

            comment = st.text_area(label='DETAILS OF TRANSACTION')

            bill_date = datetime.now()
            submit  = st.form_submit_button(label="POST BILL")

            if submit:
                if (not description or not charges):
                    st.warning("🚨 MAKE SURE ALL ASTERISKED SECTIONS ARE FILLED BEFORE SUBMITTING!")
                    st.stop()
                else:
                    query = """INSERT INTO TRANSACTION
                    (ROOM_NUMBER, ID_NUMBER, DESCRIPTION, CHARGES, COMMENT, DATE)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
                    values = (room, bill_no, description, charges, comment, bill_date)

                    cursor.execute(query, values)
                    billsql.mydb.commit()
    except:
        st.warning("THERE IS AN ISSUE SOMEWHERE. YOU MAY WANT TO SEE YOUR SUPERVISOR OR I.T.")

def payment():
    try:
        paysql=MYSQL_CONNECT()
        paysql.transaction(
            db='BRAVA_HOTEL',
            table='TRANSACTION'
        )
        cursor = paysql.mydb.cursor()
        cursor.execute("USE BRAVA_HOTEL")
        cursor.execute("SELECT ROOM_NUMBER FROM IN_HOUSE")
        result = cursor.fetchall()

        from functools import reduce
        room_number = []
        for i in result:
            i = str(i)
            i = [x for x in i if x not in ["(", ")", ",", "'", "'"]]
            i = reduce(lambda a, b: a+b, i)
            room_number.append(i)

        post =[
            'LAUNDRY',
            'CAR-WASH',
            'SWIMMING POOL',
            'BAR',
            'RESTAURANT',
            'PHOTOSHOOT',
            'ACCOMODATION'
        ]

        pay_method = [
            'TRANSFER',
            'POS',
            'CASH',
            'VOUCHER',
            'COMPLEMENTARY'
        ]

        with st.form(key='BILLING', clear_on_submit=True, border=True):
            st.header("IN-HOUSE GUESTS PAYMENT ARE POSTED HERE")
            st.write("THE SECTIONS WITH DOUBLE ASTERICKS ARE COMPULSORY!!")
            
            col1, col2, col3 = st.columns(3)
            with col1.popover("SELECT ROOM TO POST BILL **:"):
                room = st.radio("SELECT ROOM HERE", options=room_number)

            bill_no = col2.text_input(label='ENTER RECEIPT NUMBER HERE:')

            with col3.popover("CHOOSE THE POSTING DEPARTMENT:"):
                description = st.radio(label='SELECT THE POST DEPARTMENT HERE: **', options=post)
            
            col1, col2 = st.columns(2)
            deposit = col1.text_input(label='CREDIT AMOUNT **')
            pay_m = ','.join(col2.multiselect(label='CHOOSE AT LEAST ONE PAYMENT METHOD HERE', options=pay_method))

            comment = st.text_area(label='DETAILS OF PAYMENT')

            bill_date = datetime.now()

            submit  = st.form_submit_button(label="POST PAYMENT")

            if submit:
                if (not description or not deposit or not pay_m):
                    st.warning("🚨 MAKE SURE ALL ASTERISKED SECTIONS ARE FILLED BEFORE SUBMITTING!")
                else:
                    query = """INSERT INTO TRANSACTION
                    (ROOM_NUMBER, ID_NUMBER, METHOD_OF_PAYMENT, DESCRIPTION, CREDITS, COMMENT, DATE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    values = (room, bill_no, pay_m, description, deposit, comment, bill_date)

                    cursor.execute(query, values)
                    paysql.mydb.commit()
    except:
        st.warning("THERE IS NO ROOM CHECKED IN FOR NOW. YOU MAY WANT TO SEE YOUR SUPERVISOR OR I.T.")

def history():
    def retrieve(retrieval_by:str, retrieval_handle:str):
        new_sql = MYSQL_CONNECT()
        cursor = new_sql.mydb.cursor()
        cursor.execute(f"""
                        USE BRAVA_HOTEL
                            """)
        query = (f"""
                        SELECT ID, GUEST_NAME, RECEPTIONIST, PHONE_NUMBER,
                        ROOM_NUMBER, ARRIVAL_DATE, DISCOUNTED_RATE, DEPOSIT,
                        BALANCE, PAYMENT_METHOD
                        FROM HISTORY
                        WHERE {retrieval_by} = '{retrieval_handle}' """)
        df = pd.read_sql(query, new_sql.mydb)
        return (df)

    tab1, tab2, tab3 = st.tabs(['GUEST NAME', 'ROOM NUMBER', 'FOLIO_ID'])
    with tab1:
        try:
            st.subheader("SEARCH BY GUEST NAME HERE")
            name = st.text_input("ENTER NAME AS REGISTERED IN THE DATABASE!!!")
            RESULT = retrieve(
                retrieval_by = 'GUEST_NAME',
                retrieval_handle= name
            )

            st.dataframe(RESULT)
        except:
            st.info("GUEST NOT FOUND!!!")

    with tab2:
        try:
            st.subheader("SEACRH BY ROOM NUMBER")
            room_number = st.text_input("ENTER ROOM NUMBER HERE")
            RESULT = retrieve(
                retrieval_by = 'ROOM_NUMBER',
                retrieval_handle = room_number
            )
            st.dataframe(pd.DataFrame(RESULT))
        except:
            st.info("THERE IS AN ISSUE SOMEWHERE, CONTACT YOUR SUPERVISOR")

    with tab3:
        st.warning('THIS FEATURE IS NOT YET AVAILABLE!!!')

def power():  
    power_sql = MYSQL_CONNECT()
    cursor = power_sql.mydb.cursor()
    power_sql.mysql_create_connect_power_start(
        db = 'BRAVA_HOTEL',
        table='START_UTILITY'
    )
    power_sql.mysql_create_connect_power_stop(
        db = 'BRAVA_HOTEL',
        table='STOP_UTILITY'
    )  

    st.header('THIS IS TO COLLECT NECESSARY INFO ON POWER SUPPLY')
    tab1, tab2 = st.tabs(['START TIME', 'END TIME'])
    with tab1:
        st.subheader("START TIME")
        col1, col2 = st.columns(2)
        utility = col1.radio("WHAT UTILITY ARE WE USING?", ['GENERATOR', 'IBEDC'])
        time = col2.time_input("START TIME", step = 60)

        submit = st.button(label = 'SUBMIT')
        if submit:
            start_date_time = datetime.now()
            cursor.execute("""
                            USE BRAVA_HOTEL
                            """)
            query = """INSERT INTO START_UTILITY (UTILITY, START_TIME, START_DATE_TIME) VALUES (%s, %s, %s)"""
            values = (utility, time, start_date_time)
            cursor.execute(query, values)
            power_sql.mydb.commit()

    with tab2:
        st.subheader("STOP TIME")
        col1, col2, col3 = st.columns(3)
        utility = col1.radio('WHAT UTILITY ARE WE LEAVING?', ['GENERATOR', 'IBEDC'])
        time = col2.time_input('STOP TIME', step = 60)

        submit = st.button('REGISTER')
        if submit:
            stop_date_time = datetime.now()
            cursor.execute("""
                            USE BRAVA_HOTEL
                            """)
            query = """INSERT INTO STOP_UTILITY (UTILITY, STOP_TIME, STOP_DATE_TIME) VALUES (%s, %s, %s)"""
            values = (utility, time, stop_date_time)
            cursor.execute(query, values)
            power_sql.mydb.commit()

def room_transfer():
    transSQL = MYSQL_CONNECT()
    cursor = transSQL.mydb.cursor()
    transSQL.transfers(db = "BRAVA_HOTEL",
                       table= "ROOM_TRANSFERS")
    st.header("TO EFFECT GUEST ROOM TRANSFERS IN BRAVA'S DATABASE")
    with st.form(key='TRANSFERS', clear_on_submit=True, border=True):
        col1, col2 = st.columns(2)
        cursor.execute('USE BRAVA_HOTEL')
        cursor.execute('SELECT ROOM_NUMBER FROM IN_HOUSE')
        result = cursor.fetchall()
        
        from functools import reduce
        room_number = []
        for i in result:
            i = str(i)
            i = [x for x in i if x not in ["(", ")", ",", "'", "'"]]
            i = reduce(lambda a, b: a+b, i)
            room_number.append(i)

        reason = [
            'WATER-HEATER',
            'AIR-CON',
            'INTERNET',
            'T/V',
            'OTHER'
        ]

        with col1.popover('SELECT CURRENT ROOM HERE'):
            former_room = st.radio(label="CHOOSE A ROOM BELOW:", options=room_number)
        new_room = col2.text_input(label = 'ENTER NEW ROOM HERE', max_chars=3)
        details = ','.join(st.multiselect("ENTER REASON FOR ROOM CHANGE", options=reason))
        transfer_time = datetime.now()

        submit = st.form_submit_button(label="TRANSFER")
        if submit:
            if (not former_room or not details or not new_room):
                st.warning("You have not selected all the fields")
                st.stop()
            elif new_room in room_number:
                st.warning('The room is occuppied! Check out the room or change the room number!')
                st.stop()
            else:
                # STEP 1
                query = "INSERT INTO ROOM_TRANSFERS (FORMER_ROOM, DETAILS, NEW_ROOM, DATE_TIME) VALUES (%s, %s, %s, %s)"
                values = (former_room, details, new_room, transfer_time)
                cursor.execute(query, values)
                transSQL.mydb.commit()
                # STEP 2
                query = f"UPDATE IN_HOUSE SET ROOM_NUMBER = '{new_room}' WHERE ROOM_NUMBER = '{former_room}'"
                cursor.execute(query)
                transSQL.mydb.commit()
                st.rerun()

def reservation():
    rsvSQL = MYSQL_CONNECT()
    rsvSQL.reservation(db = "BRAVA_HOTEL",
                        table = "RESERVATION")
    st.header("KINDLY RESERVE YOUR GUESTS HERE:")

    def successful():
        msg = st.toast('READING INFO...')
        sleep(1)
        msg.toast('Recording data into database', icon='✍️')
        sleep(1)
        msg.toast(f'Remember to appreciate {name} for patronizing us...', icon='😁')
    
    with st.expander('OPEN HERE TO RESERVE YOUR YOUR GUESTS', icon='😁'):
        with st.form(key='RSV', clear_on_submit=True, border=True):
            st.markdown('THE AREAS MARKED ** ARE COMPULSORY!!!')
            col1, col2 = st.columns(2)
            name  = col1.text_input(label='GUEST NAME**')
            cont_info = col2.text_input(label = "PHONE NUMBER OR EMAIL ADDRESS")
            col1, col2, col3 = st.columns(3)
            arrival_date = col1.date_input(label="ARRIVAL DATE **")
            duration = col2.number_input(label="HOW MANY NIGHTS? **",step=1, min_value=1)
            ROOM_CATEGORY = [
                'BRAVA MINI ROOM',
                'STANDARD ROOM',
                'DELUXE ROOM',
                'EXECUTIVE SUITE @ 80,000',
                'EXECUTIVE SUITE @ 100,000',
                'EXECUTIVE TERRACE',
                'PRESIDENTIAL SUITE @ 120,000',
                'PRESIDENTIAL SUITE @ 150,000'
            ]
            with col3.popover(label="CLICK HERE TO SEE ROOM CATEGORIES"):
                room_cat = st.radio(label = "SELECT A CATEGORY HERE:",options=ROOM_CATEGORY)

            col1, col2, col3 = st.columns(3)
            pax = col1.number_input(label="HOW MANY ROOMS? **", min_value=1, max_value=30, step=1)
            rate = col2.text_input(label="RATE PER ROOM **", help="LEAVE IT AT ZERO FOR COMPLEMENTARY GUESTS OR VOUCHER GUESTS!")
            try:
                if isinstance(int(rate), int):
                    rate = int(rate)
                else:
                    st.warning("YOU SHOULD ENTER ONLY FIGURES!!!")
                    st.stop()
            except:
                pass

            deposit = col3.text_input(label = "HOW MUCH WAS PAID?", help=" DO NOT INPUT ANYTHING IF GUEST DID NOT PAY!", value=0)
            try:
                if isinstance(int(deposit), int):
                    deposit = int(deposit)
                else:
                    st.warning("YOU SHOULD ENTER ONLY FIGURES!!!")
                    st.stop()
            except:
                pass
            
            col1, col2 = st.columns(2)
            balance = col1.text_input(label="HOW MUCH IS THE GUEST OWING US?", value= 0)
            try:
                if isinstance(int(balance), int):
                    balance = int(balance)
                else:
                    st.warning("YOU SHOULD ENTER ONLY FIGURES!!!")
                    st.stop()
            except:
                pass

            request = col2.text_area(label = "GUEST REQUESTS")

            col1, col2 = st.columns(2)
            comment = col1.text_area(label="ADDITIONAL COMMENTS")
            
            submit = st.form_submit_button(label='RESERVE GUEST.')
            if submit:
                if not name or not duration or not rate or not pax:
                    st.warning("ENSURE YOU FILL ALL COMPULSORY FIELDS!!!")
                    st.stop()
                else:
                    cursor = rsvSQL.mydb.cursor()
                    query = """INSERT INTO RESERVATION (GUEST_NAME, CONTACT_INFO, ARRIVAL_DATE, DURATION, ROOM_CATEGORY, PAX, RATE, DEPOSIT, BALANCE, REQUEST, COMMENT)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (name.upper(), cont_info, arrival_date, duration, room_cat, pax, rate, deposit, balance, request, comment)
                    cursor.execute(query, values)
                    rsvSQL.mydb.commit()
                    successful()

    with st.expander(label="CLICK BELOW TO SEE RESERVATION TABLE: 👇", expanded=False):
        query = "SELECT * FROM RESERVATION;"
        df = pd.read_sql(query, rsvSQL.mydb)
        st.dataframe(df)

    with st.expander("SEE BELOW TO DRILL INFO FROM RESERVATION TABLE: 👇", expanded=True):
        query = "SELECT * FROM RESERVATION;"
        df = pd.read_sql(query, rsvSQL.mydb)

        dynamic_filters = DynamicFilters(df=df, filters=['GUEST_NAME', 'ARRIVAL_DATE', 'ROOM_CATEGORY', 'PAX'])
        dynamic_filters.display_filters(location='columns', num_columns=2, gap='large')
        dynamic_filters.display_df()

if __name__ == "__main__":
    st.set_page_config(
    page_title="BRAVA HOTEL",
    page_icon="🏩",
    layout="wide",
    initial_sidebar_state="auto",
) 
    
    function_pages = {
    'INTRO':intro,
    'GUEST CHECK-IN':guest_check_in,
    'GUEST CHECK-OUT':guest_checkout,
    'ROOM TRANSFER': room_transfer,
    'BILLING':posting,
    'RESERVATION':reservation,
    'PAYMENT':payment,
    'HISTORY':history,
    'UTILITY MONITOR':power
}
    options = st.sidebar.selectbox('CHOOSE AN ACTION HERE:', function_pages.keys())
    function_pages[options]()
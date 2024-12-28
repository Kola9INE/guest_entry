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

DATABASE = 'SAMPLE_HOTEL'

def greet():
    time = datetime.now().strftime("%H:%M:%S")
    hour = time.split(":")[0]
    if hour >= '00' and hour <= '11':
        return ('E&#803; KA&#x0301;A&#x0300;RO O! 🌇')
    elif hour >= '12' and hour < '16':
        return('E&#803 KA&#x0301;SA&#x0300;AN O!🌞')
    else:
        return ('E&#803 KA&#x0301;ALE&#x0301; O! 🌆')
    return

def intro():
    st.title('👨‍💼')
    st.header(f"""
                {greet()}\n
                * THIS IS THE {DATABASE}'s GUEST MANAGEMENT SOFTWARE. \n
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
            # **st.secrets['connection']
		db_host = st.secrets['connection']['host'],
		db_user = st.secrets['connection']['username'],
		db_password = st.secrets['connection']['password'],
	    	db_database = st.secrets['connection']['database']
        )

        cursor = self.mydb.cursor()
        cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {DATABASE}""")
        cursor.execute(f"""USE {DATABASE}""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS HISTORY (
                       ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       FOLIO_NUMBER INT NOT NULL,
                       RESERVATION_ID INT,
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
                       ROOM_NUMBER VARCHAR(20) NOT NULL,
                       ACTUAL_DEPARTURE DATE,
                       SPECIAL_REQUESTS SET('NON SMOKING ROOM', 'EXTRA PILLOWS', 'BABY CRIB', 'LATE CHECK OUT', 'CAR PARK VIEW') DEFAULT NULL,
                       OTHER_SPECIAL_REQUESTS TEXT DEFAULT NULL,
                       ROOM_RATE MEDIUMINT UNSIGNED NOT NULL,
                       DISCOUNTED_RATE VARCHAR(50) NOT NULL,
                       TOTAL_CREDIT BIGINT UNSIGNED,
                       TOTAL_CHARGE INT UNSIGNED,
                       BALANCE BIGINT SIGNED,
                       REFEREE VARCHAR(50) DEFAULT NULL);""")

    def mysql_create_connect_checkin(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f'USE {db}')
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}
                       ( FOLIO_NUMBER INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
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
                       DISCOUNTED_RATE VARCHAR(50) NOT NULL,
                       RESERVATION_ID INT,
                       REFEREE VARCHAR(50) DEFAULT NULL)""")
            
    def mysql_create_connect_power_start(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db}')
        cursor.execute(f'USE {db}')
        cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS {table}
                        (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                        UTILITY VARCHAR(50) NOT NULL,
                        START_TIME VARCHAR(20),
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
                        STOP_TIME VARCHAR(20),
                        STOP_DATE_TIME TIMESTAMP)""")
        return
    
    def transaction(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        cursor.execute(f"USE {db}")
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS {table}
                       (TRANSACTION_ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       FOLIO_NUMBER INT NOT NULL,
                       ROOM_NUMBER INT NOT NULL,
                       INVOICE_ID VARCHAR(10) DEFAULT NULL,
                       DESCRIPTION VARCHAR(50) NOT NULL,
                       CHARGES INT NOT NULL DEFAULT '0',
                       CREDITS INT NOT NULL DEFAULT '0',
                       METHOD_OF_PAYMENT VARCHAR(50),
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
                       GUEST_NAME VARCHAR(200) DEFAULT NULL,
                       FOLIO_NUMBER INT NOT NULL,
                       FORMER_ROOM INT NOT NULL,
                       DETAILS SET('WATER-HEATER', 'AIR-CON', 'INTERNET', 'T/V', 'OTHER') DEFAULT 'OTHER',
                       NEW_ROOM INT NOT NULL,
                       DATE_TIME TIMESTAMP)""")
        
    def reservation(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        cursor.execute(f"USE {db}")
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table}
                       (RESERVATION_ID INT PRIMARY KEY AUTO_INCREMENT,
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
                       COMMENT TEXT,
                       RSV_DATE DATE,
                       DISCOUNT VARCHAR(20) NOT NULL DEFAULT '0',
                       RECEPTIONIST VARCHAR(30) NOT NULL DEFAULT ' ')
                       """)

def guest_check_in():
    st.header(f"""{greet()}""")
    with st.form(key = 'NEW_FORM', clear_on_submit = True, border = True):
        st.title(f"""{DATABASE} GUEST REGISTRATION FORM 📃 🖋️""")
        st.write('THE SECTIONS MARKED ** ARE COMPULSORY!')
        col1, col2, col3 = st.columns(3)
        guest_name = col1.text_input(label = 'GUEST NAME**')
        rsv_id = col2.text_input('ENTER RESERVATION ID HERE.', help='LEAVE IT AT ZERO IF THERE WAS NO PRIOR RESERVATION MADE!', value='0')
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
        room_number = col3.selectbox(label = 'ROOM NUMBER **', options=list(range(1, 1001, 1)))
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
        referee = col4.text_input(label="INPUT GUEST REFERENCE HERE.", help="Who referred the guest? Leave it blank if no one.")
        submit_form = st.form_submit_button('REGISTER')
        
        if submit_form:
            try:
                new_sql = MYSQL_CONNECT()
                new_sql.mysql_create_connect_checkin(
                    db = DATABASE,
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
                    room_check.append(int(i))

                if (room_number in room_check):
                    st.warning('ROOM HAS NOT BEEN CHECKED OUT!!!')
                    st.stop()
                elif (not arr_date or not no_of_nights or not fd_name or not id_means):
                    st.warning('Make sure you fill all asterisked sections!!!')
                    st.stop()
                elif (not room_number or not rack_rate or not discounted_rate):
                    st.warning('Make sure you fill all asterisked sections!!!')
                    st.stop()
                elif (not guest_name or not country or not phone_no or not identification):
                    st.warning('Make sure you fill all asterisked parts!!!')
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
                    OTHER_SPECIAL_REQUESTS, ROOM_RATE, DISCOUNTED_RATE, RESERVATION_ID, REFEREE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    value = (guest_name.upper(), fd_name.upper(), guest_address,
                                city, state, postal_code, country,
                                phone_no, email, nationality,
                                amt_of_guests, identification, id_means,
                                arr_date, arr_time, no_of_nights, room_number,
                                expected_departure, requests, other_req, rack_rate,
                                discounted_rate, rsv_id, referee)
                    
                    cursor.execute(check_in_query, value)
                    new_sql.mydb.commit()
            except:
                with st.snow():
                    sleep(2)
                st.warning("THERE IS SOMETHING WRONG SOMEWHERE. PLEASE CONTACT YOUR SOFTWARE ADMINISTRATOR...")
                st.stop()

    st.divider()
    with st.expander('SEE IN_HOUSE GUESTS HERE: ', expanded = False):
        in_house = MYSQL_CONNECT()
        in_house.mysql_create_connect_checkin(
                    db = DATABASE,
                    table = 'IN_HOUSE'
                )
        
        st.subheader('IN HOUSE GUESTS')
        query = f'SELECT FOLIO_NUMBER, GUEST_NAME, ARRIVAL_DATE, ROOM_NUMBER, RESERVATION_ID FROM IN_HOUSE;'
        df = pd.read_sql(query, in_house.mydb)
        df['ROOM_NUMBER'] = df['ROOM_NUMBER'].astype('int')
        st.table(df)
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
                sheet.column_dimensions['C'].width = 30
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
        cursor.execute(f"""USE {DATABASE}""")
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
            room_number = st.selectbox("PICK A ROOM TO CHECK OUT HERE:", options=room_number)

        st.subheader("DETAILS OF CHECKOUT ROOM")
        query = f'''
                SELECT inh.guest_name, t.room_number, t.folio_number, t.description, t.charges, t.credits,
                CONCAT(EXTRACT(day FROM date), '-', EXTRACT(month FROM date), '-', EXTRACT(year FROM date)) AS transaction_date
	            FROM transaction t
                JOIN in_house inh
                ON inh.folio_number = t.folio_number
	            WHERE t.folio_number = (
                SELECT 
                    folio_number
                    FROM in_house
                    WHERE room_number = '{room_number}')
                        '''
        df = pd.read_sql(query, chekoutsql.mydb)
        df['transaction_date'] = df['transaction_date'].apply(pd.to_datetime)

        charges = sum(df['charges'])
        credits = sum(df['credits'])
        balance = charges - credits
        st.dataframe(df)

        col1, col2, col3 = st.columns(3)
        col1.metric('TOTAL CHARGES', charges)
        col2.metric('TOTAL CREDITS', credits)
        col3.metric('BALANCE', balance)      

        with st.popover('EXPAND HERE TO CHECK OUT ROOM'):
            check_out = st.button("CHECK OUT")

            if check_out:
                cursor.execute(f"""INSERT INTO history (folio_number, reservation_id, guest_name, receptionist, address, city, state, postal_code,
                            country, phone_number, email_address, nationality, amount_of_guests, id_number, id_means, arrival_date, arrival_time,
                            room_number, actual_departure, special_requests, other_special_requests, room_rate, discounted_rate, referee)
                                SELECT inh.folio_number, inh.reservation_id, inh.guest_name, inh.receptionist, inh.address, inh.city, inh.state,
                                inh.postal_code, inh.country, inh.phone_number, inh.email_address, inh.nationality, inh.amount_of_guests, inh.id_number,
                                inh.id_means, inh.arrival_date, inh.arrival_time, inh.room_number, current_date(), inh.special_requests, inh.other_special_requests,
                                inh.room_rate, inh.discounted_rate, referee
                                FROM in_house inh
                                JOIN transaction t
                                ON t.folio_number = inh.folio_number
                                WHERE inh.folio_number = (
                                SELECT folio_number
                                FROM in_house
                                WHERE room_number = '{room_number}')
                                LIMIT 1;
                                """)
                chekoutsql.mydb.commit()

                cursor.execute(f"""UPDATE history
                            SET total_credit = {credits},
                            total_charge = {charges},
                            balance = {balance}
                            WHERE folio_number = (SELECT folio_number
                            FROM in_house
                            WHERE room_number = {room_number})""")
                chekoutsql.mydb.commit()

                st.toast('PLEASE WAIT...')
                sleep(1)
                st.toast('ADJUSTING DATABASE...')
                sleep(1)
                st.toast("SUCCESFULL!")
                sleep(1)
                st.toast("PLEASE APPRECIATE OUR GUEST'S PATRONAGE")
                sleep(1)
                st.toast("CLICK OUT OF THE CHECK-OUT BOX")

                cursor.execute(f"""DELETE FROM IN_HOUSE WHERE room_number = {room_number}""")
                chekoutsql.mydb.commit()
                st.success(f"SUCCESSFULLY CHECKED OUT ROOM {room_number}. YOU MAY CLICK OUT OF THE CHECK OUT BOX NOW!")
    except:
       st.warning('THE SELECTED ROOM IS NOT IN_HOUSE...')

def posting():
    try:
        billsql=MYSQL_CONNECT()
        billsql.transaction(
            db= DATABASE,
            table='TRANSACTION'
        )
        cursor = billsql.mydb.cursor()
        cursor.execute(f"USE {DATABASE}")
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
            'PHOTOSHOOT',
            'REFUND'
        ]

        with st.form(key='BILLING', clear_on_submit=True, border=True):
            st.header("IN-HOUSE GUESTS TRANSACTIONS ARE POSTED HERE")
            st.write("THE SECTIONS WITH DOUBLE ASTERICKS ARE COMPULSORY!!")
            
            col1, col2, col3 = st.columns(3)
            with col1.popover("SELECT ROOM TO POST BILL **:"):
                room = st.selectbox("SELECT ROOM HERE", options=room_number)

            cursor.execute(f'USE {DATABASE}')
            query = f"SELECT FOLIO_NUMBER FROM IN_HOUSE WHERE ROOM_NUMBER = {room}"
            df = pd.read_sql(query, billsql.mydb)
            invoice_number = int(df.at[0, 'FOLIO_NUMBER'])

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
                    (FOLIO_NUMBER, ROOM_NUMBER, INVOICE_ID, DESCRIPTION, CHARGES, COMMENT, DATE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    values = (invoice_number, room, bill_no, description, charges, comment, bill_date)

                    cursor.execute(query, values)
                    billsql.mydb.commit()
                    st.success('Billing successful!')
    except:
        st.warning("THERE IS AN ISSUE SOMEWHERE. YOU MAY WANT TO SEE YOUR SUPERVISOR OR I.T.")

def payment():
    try:
        paysql=MYSQL_CONNECT()
        paysql.transaction(
            db=DATABASE,
            table='TRANSACTION'
        )
        cursor = paysql.mydb.cursor()
        cursor.execute(f"USE {DATABASE}")
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
            'FRONT-DESK'
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
                room = st.selectbox("SELECT ROOM HERE", options=room_number)

            cursor.execute(f'USE {DATABASE}')
            query = f"SELECT FOLIO_NUMBER FROM IN_HOUSE WHERE ROOM_NUMBER = {room}"
            df = pd.read_sql(query, paysql.mydb)
            invoice_number = int(df.at[0, 'FOLIO_NUMBER'])

            bill_no = col2.text_input(label='ENTER RECEIPT NUMBER HERE:')

            with col3.popover("CHOOSE THE POSTING DEPARTMENT:"):
                description = st.radio(label='SELECT THE POST DEPARTMENT HERE: **', options=post)
            
            col1, col2 = st.columns(2)
            deposit = col1.text_input(label='CREDIT AMOUNT **')
            pay_m = ', '.join(col2.multiselect(label='CHOOSE AT LEAST ONE PAYMENT METHOD HERE', options=pay_method))

            comment = st.text_area(label='DETAILS OF PAYMENT')

            bill_date = datetime.now()

            submit  = st.form_submit_button(label="POST PAYMENT")

            if submit:
                if (not description or not deposit or not pay_m):
                    st.warning("🚨 MAKE SURE ALL ASTERISKED SECTIONS ARE FILLED BEFORE SUBMITTING!")
                else:
                    query = """INSERT INTO TRANSACTION
                    (FOLIO_NUMBER, ROOM_NUMBER, INVOICE_ID, METHOD_OF_PAYMENT, DESCRIPTION, CREDITS, COMMENT, DATE)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (invoice_number, room, bill_no, pay_m, description, deposit, comment, bill_date)

                    cursor.execute(query, values)
                    paysql.mydb.commit()
                    st.success('Payment sucessful!')
    except:
        st.warning("THERE IS NO ROOM CHECKED IN FOR NOW. YOU MAY WANT TO SEE YOUR SUPERVISOR OR I.T.")

def history():
    new_sql = MYSQL_CONNECT()
    cursor = new_sql.mydb.cursor()
    def retrieve(retrieval_by:str, retrieval_handle:str):
        cursor.execute(f"""
                        USE {DATABASE}
                            """)
        query = (f"""
                        SELECT FOLIO_NUMBER, GUEST_NAME, RECEPTIONIST, PHONE_NUMBER,
                        ROOM_NUMBER, ARRIVAL_DATE, DISCOUNTED_RATE, ACTUAL_DEPARTURE,
                        TOTAL_CREDIT, TOTAL_CHARGE, BALANCE
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
            "___"
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
            "___"

            st.subheader('SUMMARY')
            st.dataframe(pd.DataFrame(RESULT))
            "___"

            query = (f"""SELECT *, date(date) as transaction_date
                        FROM transaction
                        WHERE room_number = (
                        SELECT room_number
                        FROM history
                        WHERE room_number = {room_number})
                """)
            df = pd.read_sql(query, new_sql.mydb)
            st.dataframe(df)

        except:
            st.info("THERE IS AN ISSUE SOMEWHERE, CONTACT YOUR SUPERVISOR")

    with tab3:
        try:
            st.subheader('SEARCH BY FOLIO_NUMBER')
            folio = st.text_input('ENTER FOLIO_NUMBER HERE')
            RESULT = retrieve(
                retrieval_by='FOLIO_NUMBER',
                retrieval_handle=folio
            )
            "___"
            st.dataframe(pd.DataFrame(RESULT))

            "___"
            query = (f"""SELECT *, date(date) as transaction_date
            FROM transaction
            WHERE folio_number = (
            SELECT folio_number
            FROM history
            WHERE folio_number = {folio})""")
            df = pd.read_sql(query, new_sql.mydb)
            st.dataframe(df)
        except:
            st.warning("PLEASE TRY OTHER MEANS OF SEARCHING OR TRY AGAIN, PERHAPS YOU ENTERED WRONG VALUES IN SOME FIELDS.")

def power():  
    power_sql = MYSQL_CONNECT()
    cursor = power_sql.mydb.cursor()
    power_sql.mysql_create_connect_power_start(
        db = DATABASE,
        table='START_UTILITY'
    )
    power_sql.mysql_create_connect_power_stop(
        db = DATABASE,
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
            cursor.execute(f"""
                            USE {DATABASE}
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
            cursor.execute(f"""
                            USE {DATABASE}
                            """)
            query = """INSERT INTO STOP_UTILITY (UTILITY, STOP_TIME, STOP_DATE_TIME) VALUES (%s, %s, %s)"""
            values = (utility, time, stop_date_time)
            cursor.execute(query, values)
            power_sql.mydb.commit()

    "___"
    query = """SELECT SU.ID, SU.UTILITY, SU.START_TIME, ST.STOP_TIME, ST.STOP_DATE_TIME
                FROM start_utility AS SU
                JOIN stop_utility AS ST
                ON SU.ID = ST.ID;"""
    df = pd.read_sql(query, power_sql.mydb)
    df['START_TIME'] = pd.to_datetime(df['START_TIME'])
    df['STOP_TIME'] = pd.to_datetime(df['STOP_TIME'])
    df['TIME_DIFFERENCE'] = (df['STOP_TIME'] - df['START_TIME'])
    st.dataframe(df)

def update_info():
    transSQL = MYSQL_CONNECT()
    cursor = transSQL.mydb.cursor()
    transSQL.transfers(db = DATABASE,
                       table= "ROOM_TRANSFERS")
    st.header(f"TO EFFECT GUEST ROOM TRANSFERS IN {DATABASE}'S DATABASE")
    with st.form(key='TRANSFERS', clear_on_submit=True, border=True):
        col1, col2 = st.columns(2)
        cursor.execute(f'USE {DATABASE}')
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
            former_room = st.selectbox(label="CHOOSE A ROOM BELOW:", options=room_number)
        
        cursor.execute(f'USE {DATABASE}')
        try:
            query = f"SELECT FOLIO_NUMBER, GUEST_NAME FROM IN_HOUSE WHERE ROOM_NUMBER = {former_room}"
            df = pd.read_sql(query, transSQL.mydb)
            invoice_number = int(df.at[0, 'FOLIO_NUMBER'])
            name = str(df.at[0, 'GUEST_NAME'])

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
                    query = "INSERT INTO ROOM_TRANSFERS (GUEST_NAME, FOLIO_NUMBER, FORMER_ROOM, DETAILS, NEW_ROOM, DATE_TIME) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (name, invoice_number, former_room, details, new_room, transfer_time)
                    cursor.execute(query, values)
                    transSQL.mydb.commit()
                    # STEP 2
                    query = f"UPDATE IN_HOUSE SET ROOM_NUMBER = '{new_room}' WHERE FOLIO_NUMBER = '{invoice_number}'"
                    cursor.execute(query)
                    transSQL.mydb.commit()
                    st.rerun()
        except:
            st.info('THERE IS NO ROOM IN_HOUSE')

def reservation():
    rsvSQL = MYSQL_CONNECT()
    rsvSQL.reservation(db = DATABASE,
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
            rsv_date = datetime.now().strftime("%Y:%m:%d")
            rsv_date = datetime.strptime(rsv_date, "%Y:%m:%d")
            duration = col2.number_input(label="HOW MANY NIGHTS **", step=1, min_value=1)

            ROOM_CATEGORY = [
                'PHOTOSHOOT',
                'BRAVA MINI ROOM',
                'STANDARD ROOM',
                'DELUXE ROOM',
                'EXECUTIVE SUITE @ 80,000',
                'EXECUTIVE SUITE @ 100,000',
                'EXECUTIVE TERRACE',
                'PRESIDENTIAL SUITE @ 120,000',
                'PRESIDENTIAL SUITE @ 150,000'
            ]
            with col3.popover(label="CLICK HERE TO SEE CATEGORIES"):
                room_cat = st.selectbox(label = "SELECT A CATEGORY HERE:",options=ROOM_CATEGORY)

            col1, col2, col3 = st.columns(3)
            pax = col1.number_input(label="HOW MANY ROOMS? **", min_value=0, max_value=30, step=1)
            rate = col2.text_input(label="RATE PER ROOM/SESSION **", help="LEAVE IT AT ZERO FOR COMPLEMENTARY GUESTS OR VOUCHER GUESTS!")
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

            col1, col2, col3 = st.columns(3)
            comment = col1.text_area(label="ADDITIONAL COMMENTS (RECEPTIONIST'S REMARK)")
            receptionist = col2.text_input('NAME OF RECEPTIONIST **', max_chars=20)
            discount = col3.text_input(label = 'DISCOUNT APPLIED', help='LEAVE AT ZERO IF NO DISCOUNT WAS APPLIED!', value='0')
            submit = st.form_submit_button(label='RESERVE GUEST.')
            if submit:
                if not name or not duration or not rate or not pax:
                    st.warning("ENSURE YOU FILL ALL COMPULSORY FIELDS!!!")
                    st.stop()
                else:
                    cursor = rsvSQL.mydb.cursor()
                    query = """INSERT INTO RESERVATION (GUEST_NAME, CONTACT_INFO, ARRIVAL_DATE, DURATION, ROOM_CATEGORY, PAX, RATE, DEPOSIT, BALANCE, REQUEST, COMMENT, RECEPTIONIST, RSV_DATE, DISCOUNT)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    values = (name.upper(), cont_info, arrival_date, duration, room_cat, pax, rate, deposit, balance, request, comment, receptionist.upper(), rsv_date, discount)
                    cursor.execute(query, values)
                    rsvSQL.mydb.commit()
                    successful()

    with st.expander(label="CLICK BELOW TO SEE RESERVATION TABLE:", expanded=False):
        query = "SELECT * FROM RESERVATION;"
        df = pd.read_sql(query, rsvSQL.mydb)
        st.dataframe(df)

    with st.expander("SEE BELOW TO DRILL INFO FROM RESERVATION TABLE:", expanded=False):
        query = "SELECT * FROM RESERVATION;"
        df = pd.read_sql(query, rsvSQL.mydb)

        rsv_filters = DynamicFilters(df=df, filters=['GUEST_NAME', 'ARRIVAL_DATE', 'ROOM_CATEGORY', 'PAX', 'RSV_DATE', 'RECEPTIONIST'])
        rsv_filters.display_filters(location='columns', num_columns=3, gap='small')
        rsv_filters.display_df()

def for_audit():
    st.warning('CAUTION! FOR AUDIT PURPOSES ONLY!', icon = "🛑")
    auditSQL = MYSQL_CONNECT()
    auditSQL.transaction(
        db = DATABASE,
        table = 'TRANSACTION'
    )
    cursor = auditSQL.mydb.cursor()
    cursor.execute(f'USE {DATABASE}')
    query = f'SELECT *, date(date) as TRANSACTION_DATE FROM TRANSACTION'
    st.subheader('SEE TRANSACTIONS BELOW:')
    audit_df = pd.read_sql(query, auditSQL.mydb)

    '___'
    with st.sidebar:
        dynamic_filters = DynamicFilters(audit_df, filters=['TRANSACTION_DATE', 'DESCRIPTION'])
    
    dynamic_filters.display_filters(location='sidebar')
    dynamic_filters.display_df()

    '___'
    cursor.execute(f'USE {DATABASE}')
    query2 = f"SELECT GUEST_NAME, FORMER_ROOM, DETAILS AS 'REASONS_FOR_CHANGE', NEW_ROOM, DATE(DATE_TIME) AS 'TRANSFER_DATE' FROM ROOM_TRANSFERS"
    st.subheader('SEE ROOM TRANSFERS BELOW:')
    df = pd.read_sql(query2, auditSQL.mydb)
    st.dataframe(df)

if __name__ == "__main__":
    st.set_page_config(
    page_title=f"{DATABASE}",
    page_icon="🏩",
    layout="wide",
    initial_sidebar_state="auto",
) 
    print(f'\nLOG ISSUES @ {datetime.now().strftime('%H:%M:%S')} (THIS IS NOT AN ISSUE. ONLY CRITICAL ISSUES WILL CRASH THE APP)')
    
    function_pages = {
    'INTRO':intro,
    'GUEST CHECK-IN':guest_check_in,
    'GUEST CHECK-OUT':guest_checkout,
    'UPDATE INFO': update_info,
    'BILLING':posting,
    'RESERVATION':reservation,
    'PAYMENT':payment,
    'HISTORY':history,
    'UTILITY MONITOR':power,
    'AUDIT':for_audit
}
    options = st.sidebar.selectbox('CHOOSE AN ACTION HERE:', function_pages.keys())
    function_pages[options]()

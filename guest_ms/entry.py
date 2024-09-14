"""
CONSIDER THIS AS A WORK-IN-PROGRESS, OR AN 'MVP'.
This is a software that loads a streamlit form on localhost to capture guests' data as entered 
the front desk officer and stores on a MySql database.
This is to have a database to hold hotel's guest checkin history.

It loads guests data to check_in table, on check_out it loads it history table in the database
"""

import streamlit as st
import mysql.connector, toml, pandas as pd
from datetime import datetime, timedelta
from time import sleep

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
        with open(r'C:\Users\HP\Desktop\guest_entry\guest_ms\conn.toml', 'r') as file:
            config = toml.load(file)

        self.mydb = mysql.connector.connect(
            host = config['connection']['host'],
            user = config['connection']['user'],
            password = config['connection']['password']
        )
        return
    
    def mysql_create_connect_history(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"""CREATE DATABASE IF NOT EXISTS {db}""")
        cursor.execute(f"""USE {db}""")
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
                       ACTUAL_DEPARTURE DATE,
                       SPECIAL_REQUESTS SET('NON SMOKING ROOM', 'EXTRA PILLOWS', 'BABY CRIB', 'LATE CHECK OUT', 'CAR PARK VIEW') DEFAULT NULL,
                       OTHER_SPECIAL_REQUESTS TEXT DEFAULT NULL,
                       ROOM_RATE MEDIUMINT UNSIGNED NOT NULL,
                       DISCOUNTED_RATE VARCHAR(50) NOT NULL,
                       DEPOSIT BIGINT UNSIGNED NOT NULL,
                       BALANCE BIGINT SIGNED NOT NULL DEFAULT '0',
                       PAYMENT_METHOD ENUM('TRANSFER', 'COMPLEMENTARY', 'POS', 'CASH', 'VOUCHER') DEFAULT 'TRANSFER')""")
        return
    
    def mysql_create_connect_checkin(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {db}')
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
                       DISCOUNTED_RATE VARCHAR(50) NOT NULL,
                       DEPOSIT BIGINT UNSIGNED NOT NULL,
                       PAYMENT_METHOD ENUM('TRANSFER', 'COMPLEMENTARY', 'POS', 'CASH', 'VOUCHER') DEFAULT 'TRANSFER')""")
            
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
    
    def billing(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        cursor.execute(f"USE {db}")
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS {table}
                       (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       ROOM_NUMBER INT NOT NULL,
                       POSTING VARCHAR(50) NOT NULL,
                       AMOUNT INT NOT NULL,
                       BILL_ID VARCHAR(10) DEFAULT NULL,
                       COMMENT TEXT,
                       BILL_DATE DATETIME
                       )""")
        return
    
    def payment(self, db:str, table:str):
        cursor = self.mydb.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db}")
        cursor.execute(f"USE {db}")
        cursor.execute(f"""
                       CREATE TABLE IF NOT EXISTS {table}
                       (ID INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
                       ROOM_NUMBER INT NOT NULL,
                       PAYMENT_FOR ENUM('LAUNDRY', 'BAR', 'PHOTOSHOOT', 'RESTAURANT', 'ACCOMODATION') DEFAULT 'RESTAURANT',
                       AMOUNT INT NOT NULL,
                       PAYMENT_ID VARCHAR(10) NOT NULL DEFAULT '0',
                       COMMENT TEXT,
                       PAY_DATE DATETIME)
                       """)

def guest_check_in():
    st.header(f"""{greet()}""")
    st.title("""BRAVA HOTEL GUEST REGISTRATION FORM 📃 🖋️""")
    with st.form(key = 'NEW_FORM', clear_on_submit = True, border = True):
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
        deposit = col3.text_input(label = 'DEPOSIT **', value='0')

        method_of_payment = [
            'TRANSFER',
            'COMPLEMENTARY',
            'POS',
            'CASH',
            'VOUCHER'
        ]
        with col4.popover('METHOD OF PAYMENT**'):
            m_o_p = ','.join(st.multiselect(label = 'CHOOSE AT LEAST ONE OF THE FOLLOWING.', options = method_of_payment))

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

                if (not guest_name or not country or not phone_no or not deposit or not identification):
                    st.warning('Make sure you fill all asterisked parts!!!')
                    st.stop()
                elif (not arr_date or not no_of_nights or not fd_name or not id_means):
                    st.warning('Make sure you fill all asterisked sections!!!')
                    st.stop()
                elif (not room_number or not rack_rate or not discounted_rate or not m_o_p):
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
                    OTHER_SPECIAL_REQUESTS, ROOM_RATE, DISCOUNTED_RATE, 
                    DEPOSIT, PAYMENT_METHOD)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                    value = (guest_name, fd_name, guest_address,
                                city, state, postal_code, country,
                                phone_no, email, nationality,
                                amt_of_guests, identification, id_means,
                                arr_date, arr_time, no_of_nights, room_number,
                                expected_departure, requests, other_req, rack_rate,
                                discounted_rate, deposit, m_o_p)
                    
                    cursor.execute(check_in_query, value)
                    new_sql.mydb.commit()
            except:
                with st.snow():
                    sleep(2)
                st.warning("THERE IS SOMETHING WRONG SOMEWHERE. PLEASE CONTACT YOUR SOFTWARE ADMINISTRATOR...")
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
            room_number = st.radio("PICK ONE OR MORE ROOMS TO CHECK OUT HERE:", options=room_number)

        st.subheader("DETAILS OF CHECKOUT ROOM")
        query = f"SELECT GUEST_NAME, PHONE_NUMBER, AMOUNT_OF_GUESTS, ARRIVAL_DATE, EXPECTED_DEPARTURE, ROOM_NUMBER, ROOM_RATE, DISCOUNTED_RATE, DEPOSIT FROM IN_HOUSE WHERE ROOM_NUMBER = {room_number}"
        df = pd.read_sql(query, chekoutsql.mydb)
        df['DISCOUNTED_RATE'] = df['DISCOUNTED_RATE'].astype(int)
        st.dataframe(df)

        name, phone_number, arrival_date, expected_dep, room_no, room_rate, discounted_rate, deposit = (df.at[0, 'GUEST_NAME'],
                                                                                        df.at[0, 'PHONE_NUMBER'],
                                                                                        df.at[0, 'ARRIVAL_DATE'],
                                                                                        df.at[0, 'EXPECTED_DEPARTURE'],
                                                                                        df.at[0, 'ROOM_NUMBER'],
                                                                                        df.at[0, 'ROOM_RATE'],
                                                                                        df.at[0, 'DISCOUNTED_RATE'],
                                                                                        df.at[0, 'DEPOSIT'])
        arrival_date_new = str(arrival_date)
        arrival_date_new = datetime.strptime(arrival_date_new, "%Y-%m-%d")
        check_out_day = datetime.now().strftime("%Y-%m-%d")
        check_out_day_new = datetime.strptime(check_out_day, "%Y-%m-%d")
        day_diff = (check_out_day_new - arrival_date_new).days
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
    except:
        st.warning('THERE IS NO ROOM TO CHECK OUT YET...')

def posting():
    try:
        billsql=MYSQL_CONNECT()
        billsql.billing(
            db='BRAVA_HOTEL',
            table='BILLING'
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
            'BAR',
            'RESTAURANT',
            'PHOTOSHOOT',
            'ACCOMODATION'
        ]

        with st.form(key='BILLING', clear_on_submit=True, border=True):
            st.header("IN-HOUSE GUESTS TRANSACTIONS ARE POSTED HERE")
            st.write("THE SECTIONS WITH DOUBLE ASTERICKS ARE COMPULSORY!!")
            
            col1, col2, col3 = st.columns(3)
            with col1.popover("SELECT ROOM TO POST BILL **:"):
                room = st.radio("SELECT ROOM HERE", options=room_number)


            post_addr = col2.radio(label='SELECT THE POST DEPARTMENT HERE: **', options=post)
            amount = col3.text_input(label='AMOUNT **')

            col1, col2 = st.columns(2)
            bill_no = col1.text_input(label='BILL-ID:')
            details = col2.text_area(label='DETAILS OF TRANSACTION')

            bill_date = datetime.now()
            submit  = st.form_submit_button(label="POST BILL")

            if submit:
                if (not post_addr or not amount):
                    st.warning("🚨 MAKE SURE ALL ASTERISKED SECTIONS ARE FILLED BEFORE SUBMITTING!")
                else:
                    query = """INSERT INTO BILLING
                    (ROOM_NUMBER, POSTING, AMOUNT,
                     BILL_ID, COMMENT, BILL_DATE)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
                    values = (room, post_addr, amount, bill_no, details, bill_date)

                    cursor.execute(query, values)
                    billsql.mydb.commit()
    except:
        st.warning("THERE IS NO ROOM CHECKED IN FOR NOW. YOU MAY WANT TO SEE YOUR SUPERVISOR OR I.T.")

def payment():
    try:
        billsql=MYSQL_CONNECT()
        billsql.payment(
            db='BRAVA_HOTEL',
            table='PAYMENT'
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
            'BAR',
            'RESTAURANT',
            'PHOTOSHOOT',
            'ACCOMODATION'
        ]

        with st.form(key='PAYMENT', clear_on_submit=True, border=True):
            st.header("IN-HOUSE GUESTS PAYMENTS ARE POSTED HERE")
            st.write("THE SECTIONS WITH DOUBLE ASTERICKS ARE COMPULSORY!!")
            
            col1, col2, col3 = st.columns(3)
            with col1.popover("SELECT ROOM TO POST PAYMENT **:"):
                room = st.radio("SELECT ROOM HERE", options=room_number)


            pay_addr = ','.join(col2.multiselect(label='SELECT THE POST DEPARTMENT HERE: **', options=post))
            amount = col3.text_input(label='AMOUNT **')

            col1, col2 = st.columns(2)
            pay_id = col1.text_input(label='PAYMENT-ID:')
            details = col2.text_area(label='DETAILS OF PAYMENT')

            bill_date = datetime.now()
            submit  = st.form_submit_button(label="POST PAYMENT")

            if submit:
                if (not pay_addr or not amount):
                    st.warning("🚨 MAKE SURE ALL ASTERISKED SECTIONS ARE FILLED BEFORE SUBMITTING!")
                else:
                    query = """INSERT INTO PAYMENT
                    (ROOM_NUMBER, PAYMENT_FOR, AMOUNT,
                     PAYMENT_ID, COMMENT, PAY_DATE)
                    VALUES (%s, %s, %s, %s, %s, %s)"""
                    values = (room, pay_addr, amount, pay_id, details, bill_date)

                    cursor.execute(query, values)
                    billsql.mydb.commit()
    except:
        st.warning("THERE IS NO ROOM CHECKED IN FOR NOW. YOU MAY WANT TO SEE YOUR SUPERVISOR OR I.T.")

def room_info():
    with st.snow():
        sleep(3)
    st.warning("""👨‍💼 PLEASE BEAR WITH US 
                   🚧 THIS SECTION IS UNDER MAINTENANCE 🚧 👨‍💻. FOR MORE INFO SEE YOUR SUPERVISOR """)

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
                        FROM GUEST_HISTORY
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
        col1, col2 = st.columns(2)
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
    'BILLING':posting,
    'PAYMENT':payment,
    'ROOM INFORMATION': room_info,
    'HISTORY':history,
    'UTILITY MONITOR':power
}
    options = st.sidebar.selectbox('CHOOSE AN ACTION HERE:', function_pages.keys())
    function_pages[options]()
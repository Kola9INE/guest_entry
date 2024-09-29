This is a software that loads a streamlit web app on localhost to cater for the front office operations.
The aim is to create a software that handles the guests and power data of the hotel. The software has the following sections wiht its predefined function(s).

The user of this program should create a secret.toml file in the .streamlit folder on the host device as that is what the software uses to create a connection with the mysql database. 
In the secrets.toml file should be the details of the mysql connection parameter (host, user and password). It is not neccesary to include a database name in the secrets.toml file as it has been hard coded into the software. The name of the database this software have been instructed to create is the 'brava_hotel'. You may change it at your end, if you wish.

Below are the functions the software has been programmed to do:

- Check-In: This section displays a form where the front desk officer/hotel receptionist can input guests' information. 
  The inputs are stored in a mysql database by taking advantage of the python-mysql connector and relevant queries.

- Room Transfers: This section displays a form where the front desk officer/hotel receptionist can chnage the room number of an in-house guest (guest that are already lodged) inthe hotel facilities. Via the use of Mysql queries and the python-mysql connector, the change is effected on the mysql database.

- Posting: This section displays a form where the front desk officer/hotel receptionist post bills to a room. There is a table intitiated in the mysql database for the hotel where posted bills are recorded.

- Payment: This section displays a form where the front desk officer/hotel receptionist post payments to a room. There is a table intitiated in the mysql database for the hotel where posted payments are recorded.

- Reservation: This section diplays a form to collect reservation details. It also displays the reservation table  as stored in the database and equally provides filters to narrow the scope of the reservation table.

- History: THIS SECTION IS STILL IN DEVELOPMENT. The objective is to display a form that allows the user(the front desk officer) to search the hotel's database via room-number,
  guest names or folio/invoice-id. The software queries the database on the entered search parameters.

- Power: This section loads a form that records the amount of time electricity was supplied to the hotel via generetor and IBEDC. The essence of this is to keep tabs on
  electricity usage and consequently, the company's consumption of diesel.

- Check-out: THIS SECTION IS STILL IN DEVELOPMENT. The objective is to update the HISTORY table in the hotel's database on guest checkout so that checking out a guest deletes the
  guest from the hotel's 'in_house' table and updates the hotel's 'history' table with its relevant data.

  --TO DO--
  
  I am yet to:
  
  1. Integrate an END-OF-DAY algorithm.
  2. Create a shell that automates the process of opening a vscode terminal or any CLI to load the streamlit app on localhost.

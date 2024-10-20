

import singlestoredb as s2
import os

class DBConnection:

    def __init__(self):
        self.user =  os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = 'svc-3482219c-a389-4079-b18b-d50662524e8a-shared-dml.aws-virginia-6.svc.singlestore.com'
        self.port=3333
        self.database='db_mrunmayee_001f7'
        # ssl_ca='../singlestore_bundle.pem' 
        self.conn = s2.connect(
            user=self.user, 
            password=self.password, 
            host=self.host,
            port=self.port, 
            database=self.database)
        

    def getUser(self):
        email = input('Enter your email:')
        input_password = input('Enter password:')

        self.connected =self.conn.is_connected
       
        if not self.connected:
            return
    
        try:
            cursor = self.conn.cursor()  # Dictionary cursor for fetching rows as dicts
            query = "SELECT user_id, password FROM Users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()
            
            if user:
                # Compare input password with the password in the database
                if user[1] == input_password:
                    print(f"Login successful!")
                    self.user_id=user[0]
                    self.connected =True
                else:
                    print("Incorrect password!")
            else:
                print("User not found!")
            cursor.close()

        except BaseException as err:
            print(f"Error: {err}")

    # def test_db(self):
    #     cur = self.conn.cursor()
    #     # Execute SQL
    #     cur.execute('SHOW TABLES;')

    #     # Fetch the results
    #     print(cur.description)
    #     for item in cur:
    #         print(item)

    def updateUserEmotion(self, emotion = 'happy'):
        if not self.connected:
            return
    
        try:
            cursor = self.conn.cursor()
            print('Entered update')

            # SQL query to insert data into UserEmotions table
            insert_query = """
            INSERT INTO UserEmotions (user_id, emotion) 
            VALUES (%s, %s)
            """
            # Data to insert (user_id and emotion)
            data = (self.user_id, emotion)

            # Execute the query
            cursor.execute(insert_query, data)

            # Commit the transaction
            self.conn.commit()

            print(f"Emotion for user added successfully!")
        
            cursor.close()

        except BaseException as err:
            print(f"Error: {err}")


    def closeConnection(self):
        self.conn.close()
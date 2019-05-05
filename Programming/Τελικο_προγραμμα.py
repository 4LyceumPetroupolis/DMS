import RPi.GPIO as GPIO # ενεργοποιουμε τα GPIO pins
import smbus            # module για να λειτουγησει ο αισθητηρας
import pandas as pd     # εισαγουμε ενα module για να διαβασει τον πινακα
import time
x=0 # η μεταβλητη για τις ημερες
while x <= 90: # δηλαδη το πργραμμα θα τρεχει για 90 ημερες 
    pill_schedule = pd.read_csv('schedule.csv') # εδω διαβαζει τον πινακα

    time_schedule = {
    “M”:“800”,
    “N”:“1305”,
    “E”:“2000”,
    } # οριζουμε τι σημαινουν τα συμβολα του πινακα 

    while true:
    time.sleep(40) # Sleep 40 sec για να μην διαβασει 2 φορες σε 1 λεπτο
    now = time.mktime()
    today_day = time.strftime("%a", now) # ελεγχει την ημερα
    now_time = time.strftime('%H%M', now) # ελεγχει την ωρα το λεπτο και το δευτερολεπτο

    for row in pill_schedule: # ψαχνει να βρει αν στον πινακα υπαρχει συμβολο πουαντισιχει στην τωρινη ωρα
            medicine_name=row[“medicine”]
            day_schedule=row[today_day]
            time_list=[]

    for character in day_schedule.value[0]:  # check value or value[0]
                    time_list.append(time_schedule[character])

            if now_time in time_list: # δινει εντολη να τρεξει το προγραμμα για να πεσει το χαπι
                GPIO.setmode(GPIO.BOARD)
                ControlPin = [7,11,13,15] # τα GPIO pins στα οποια ειναι το μοτερ 

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

            seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin 
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1],
                     [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4):  
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
            # Get I2C bus
            bus = smbus.SMBus(1)

            bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
            bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) 
         
            time.sleep(0.1)
            data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως  
            data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως  
         
            # μετατρεπει τις μετρησεις του
            ch0 = data[1] * 256 + data[0]
            ch1 = data1[1] * 256 + data1[0]
        
            while ch0 >= 25: # αν το φως δεν μειωθει σημαινει πως το χαπι δεν επεσε για αυτο επαναλαμβανεται η κινηση του μοτερ μεχρι να πεσει το χαπι 

                bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
                bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) # δινει ενολη στον αισθητηρα να παρει μετρηση
         
                time.sleep(0.5)
                data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως
                data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως
         
                # μετατρεπει τις μετρησεις του
                ch0 = data[1] * 256 + data[0]
                ch1 = data1[1] * 256 + data1[0]

                GPIO.setmode(GPIO.BOARD)

                ControlPin = [7,11,13,15] # τα GPIO pins στα οποια ειναι το μοτερ

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

                seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin
                         [1,1,0,0],
                         [0,1,0,0],
                         [0,1,1,0],
                         [0,0,1,0],
                         [0,0,1,1],
                         [0,0,0,1],
                         [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4): # ποσες φορες θα επαναληφθει για στροφη 360 μοιρες (2048)
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                        time.sleep(0.001)
                
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(37,GPIO.OUT) # το pin στο οποιο βρισκεται ο βομβιτης 
            for x in range(0,3):
                GPIO.output(37,True) # ενεργοποιηται ο βομβιτης
            time.sleep(1)
            print ('MEDICINE TIME') # εμφανηση γραπτου μυνηματος
        GPIO.cleanup() # εκκαθαριση των GPIO pins

        

        # εκτελεση προγραμματος για το 2ο χαπι
    pill_schedule = pd.read_csv('schedule.csv') # εδω διαβαζει τον πινακα

    time_schedule = {
    “M”:“800”,
    “N”:“1305”,
    “E”:“2000”,
    } # οριζουμε τι σημαινουν τα συμβολα του πινακα 

    while true:
    time.sleep(40) # Sleep 40 sec για να μην διαβασει 2 φορες σε 1 λεπτο
    now = time.mktime()
    today_day = time.strftime("%a", now) # ελεγχει την ημερα
    now_time = time.strftime('%H%M', now) # ελεγχει την ωρα το λεπτο και το δευτερολεπτο

    for row in pill_schedule: # ψαχνει να βρει αν στον πινακα υπαρχει συμβολο πουαντισιχει στην τωρινη ωρα
            medicine_name=row[“medicine”]
            day_schedule=row[today_day]
            time_list=[]

    for character in day_schedule.value[0]:  # check value or value[0]
                    time_list.append(time_schedule[character])

            if now_time in time_list: # δινει εντολη να τρεξει το προγραμμα για να πεσει το χαπι
                GPIO.setmode(GPIO.BOARD)
                ControlPin = [29,31,33,35] # τα GPIO pins στα οποια ειναι το μοτερ 

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

            seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1],
                     [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4):  
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
            # Get I2C bus
            bus = smbus.SMBus(1)

            bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
            bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) 
         
            time.sleep(0.1)
            data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως  
            data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως  
         
            # μετατρεπει τις μετρησεις του
            ch0 = data[1] * 256 + data[0]
            ch1 = data1[1] * 256 + data1[0]
        
            while ch0 >= 25: # αν το φως δεν μειωθει σημαινει πως το χαπι δεν επεσε για αυτο επαναλαμβανεται η κινηση του μοτερ μεχρι να πεσει το χαπι 

                bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
                bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) # δινει ενολη στον αισθητηρα να παρει μετρηση
         
                time.sleep(0.5)
                data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως
                data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως
         
                # μετατρεπει τις μετρησεις του
                ch0 = data[1] * 256 + data[0]
                ch1 = data1[1] * 256 + data1[0]

                GPIO.setmode(GPIO.BOARD)

                ControlPin = [29,31,33,35] # τα GPIO pins στα οποια ειναι το μοτερ

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

                seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin
                         [1,1,0,0],
                         [0,1,0,0],
                         [0,1,1,0],
                         [0,0,1,0],
                         [0,0,1,1],
                         [0,0,0,1],
                         [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4): # ποσες φορες θα επαναληφθει για στροφη 360 μοιρες (2048)
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                        time.sleep(0.001)
                
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(37,GPIO.OUT) # το pin στο οποιο βρισκεται ο βομβιτης 
            for x in range(0,3):
                GPIO.output(37,True) # ενεργοποιηται ο βομβιτης
            time.sleep(1)
            print ('MEDICINE TIME') # εμφανηση γραπτου μυνηματος
        GPIO.cleanup() # εκκαθαριση των GPIO pins



    # εκτελεση προγραμματος για το 3ο χαπι
    pill_schedule = pd.read_csv('schedule.csv') # εδω διαβαζει τον πινακα

    time_schedule = {
    “M”:“800”,
    “N”:“1305”,
    “E”:“2000”,
    } # οριζουμε τι σημαινουν τα συμβολα του πινακα 

    while true:
    time.sleep(40) # Sleep 40 sec για να μην διαβασει 2 φορες σε 1 λεπτο
    now = time.mktime()
    today_day = time.strftime("%a", now) # ελεγχει την ημερα
    now_time = time.strftime('%H%M', now) # ελεγχει την ωρα το λεπτο και το δευτερολεπτο

    for row in pill_schedule: # ψαχνει να βρει αν στον πινακα υπαρχει συμβολο πουαντισιχει στην τωρινη ωρα
            medicine_name=row[“medicine”]
            day_schedule=row[today_day]
            time_list=[]

    for character in day_schedule.value[0]:  # check value or value[0]
                    time_list.append(time_schedule[character])

            if now_time in time_list: # δινει εντολη να τρεξει το προγραμμα για να πεσει το χαπι
                GPIO.setmode(GPIO.BOARD)
                ControlPin = [12,16,18,22] # τα GPIO pins στα οποια ειναι το μοτερ 

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

            seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1],
                     [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4):  
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
            # Get I2C bus
            bus = smbus.SMBus(1)

            bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
            bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) 
         
            time.sleep(0.1)
            data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως  
            data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως  
         
            # μετατρεπει τις μετρησεις του
            ch0 = data[1] * 256 + data[0]
            ch1 = data1[1] * 256 + data1[0]
        
            while ch0 >= 25: # αν το φως δεν μειωθει σημαινει πως το χαπι δεν επεσε για αυτο επαναλαμβανεται η κινηση του μοτερ μεχρι να πεσει το χαπι 

                bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
                bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) # δινει ενολη στον αισθητηρα να παρει μετρηση
         
                time.sleep(0.5)
                data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως
                data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως
         
                # μετατρεπει τις μετρησεις του
                ch0 = data[1] * 256 + data[0]
                ch1 = data1[1] * 256 + data1[0]

                GPIO.setmode(GPIO.BOARD)

                ControlPin = [12,16,18,22] # τα GPIO pins στα οποια ειναι το μοτερ

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

                seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin
                         [1,1,0,0],
                         [0,1,0,0],
                         [0,1,1,0],
                         [0,0,1,0],
                         [0,0,1,1],
                         [0,0,0,1],
                         [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4): # ποσες φορες θα επαναληφθει για στροφη 360 μοιρες (2048)
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                        time.sleep(0.001)
                
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(37,GPIO.OUT) # το pin στο οποιο βρισκεται ο βομβιτης 
            for x in range(0,3):
                GPIO.output(37,True) # ενεργοποιηται ο βομβιτης
            time.sleep(1)
            print ('MEDICINE TIME') # εμφανηση γραπτου μυνηματος
        GPIO.cleanup() # εκκαθαριση των GPIO pins



    # εκτελεση προγραμματος για το 4ο χαπι
    pill_schedule = pd.read_csv('schedule.csv') # εδω διαβαζει τον πινακα

    time_schedule = {
    “M”:“800”,
    “N”:“1305”,
    “E”:“2000”,
    } # οριζουμε τι σημαινουν τα συμβολα του πινακα 

    while true:
    time.sleep(40) # Sleep 40 sec για να μην διαβασει 2 φορες σε 1 λεπτο
    now = time.mktime()
    today_day = time.strftime("%a", now) # ελεγχει την ημερα
    now_time = time.strftime('%H%M', now) # ελεγχει την ωρα το λεπτο και το δευτερολεπτο

    for row in pill_schedule: # ψαχνει να βρει αν στον πινακα υπαρχει συμβολο πουαντισιχει στην τωρινη ωρα
            medicine_name=row[“medicine”]
            day_schedule=row[today_day]
            time_list=[]

    for character in day_schedule.value[0]:  # check value or value[0]
                    time_list.append(time_schedule[character])

            if now_time in time_list: # δινει εντολη να τρεξει το προγραμμα για να πεσει το χαπι
                GPIO.setmode(GPIO.BOARD)
                ControlPin = [32,36,38,40] # τα GPIO pins στα οποια ειναι το μοτερ 

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

            seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin
                     [1,1,0,0],
                     [0,1,0,0],
                     [0,1,1,0],
                     [0,0,1,0],
                     [0,0,1,1],
                     [0,0,0,1],
                     [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4):  
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                    time.sleep(0.001)
            # Get I2C bus
            bus = smbus.SMBus(1)

            bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
            bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) 
         
            time.sleep(0.1)
            data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως  
            data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως  
         
            # μετατρεπει τις μετρησεις του
            ch0 = data[1] * 256 + data[0]
            ch1 = data1[1] * 256 + data1[0]
        
            while ch0 >= 25: # αν το φως δεν μειωθει σημαινει πως το χαπι δεν επεσε για αυτο επαναλαμβανεται η κινηση του μοτερ μεχρι να πεσει το χαπι 

                bus.write_byte_data(0x39, 0x00 | 0x80, 0x03) # αναβει τον αισθητηρα 
                bus.write_byte_data(0x39, 0x01 | 0x80, 0x02) # δινει ενολη στον αισθητηρα να παρει μετρηση
         
                time.sleep(0.5)
                data = bus.read_i2c_block_data(0x39, 0x0C | 0x80, 2) # μετραει το συνολικο φως
                data1 = bus.read_i2c_block_data(0x39, 0x0E | 0x80, 2) # μετραει το IR(infared) φως
         
                # μετατρεπει τις μετρησεις του
                ch0 = data[1] * 256 + data[0]
                ch1 = data1[1] * 256 + data1[0]

                GPIO.setmode(GPIO.BOARD)

                ControlPin = [32,36,38,40] # τα GPIO pins στα οποια ειναι το μοτερ

                for pin in ControlPin:
                    GPIO.setup(pin,GPIO.OUT)
                    GPIO.output(pin,0)

                seq =  [ [1,0,0,0], # η σειρα ενεργοποιησης των pin
                         [1,1,0,0],
                         [0,1,0,0],
                         [0,1,1,0],
                         [0,0,1,0],
                         [0,0,1,1],
                         [0,0,0,1],
                         [1,0,0,1] ]

                for i in range(516):
                    for halfstep in range(8):
                        for pin in range(4): # ποσες φορες θα επαναληφθει για στροφη 360 μοιρες (2048)
                            GPIO.output(ControlPin[pin], seq[halfstep][pin])
                        time.sleep(0.001)
                
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(37,GPIO.OUT) # το pin στο οποιο βρισκεται ο βομβιτης 
            for x in range(0,3):
                GPIO.output(37,True) # ενεργοποιηται ο βομβιτης
            time.sleep(1)
            print ('MEDICINE TIME') # εμφανηση γραπτου μυνηματος
        GPIO.cleanup() # εκκαθαριση των GPIO pins
        x + 1 # καθε μερα το χ θα αυξανεται κατα 1 εωσοτου ωα φθασει 90





            

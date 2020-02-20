import libdb as db
import time
# import RPi.GPIO as GPIO
# # import MFRC522
# import signal

db_name = 'testdb'
tb_name = 'persons'
id_col = 'id_num'
mill_col = 'mill'
lathe_col = 'lathe'
machine_col = 'machine'

# TODO: may need a validity column to see if they've expired in the last 4 years? or 5 years
# TODO: possibly need to write an error correction code for sending stuff on the wifi

# gets certifications by ID num, id is a string
def mill_clearance(id_number):
    query = db.query_db(db_name, tb_name, id_col, (id_number,), (mill_col,))
    if len(query) > 0:
        return query[0][0]
    return -1
    
def lathe_clearance(id_number):
    query = db.query_db(db_name, tb_name, id_col, (id_number,), (lathe_col,))
    if len(query) > 0:
        return query[0][0]
    return -1

def machine_clearance(id_number):
    query = db.query_db(db_name, tb_name, id_col, (id_number,), (machine_col,))
    if len(query) > 0:
        return query[0][0]
    return -1

# set the person's clearance bit
def update_mill(id_number, cleared_or_not):
    db.update_entry(db_name, tb_name, id_col, id_number, (mill_col,), (cleared_or_not,))

def update_lathe(id_number, cleared_or_not):
    db.update_entry(db_name, tb_name, id_col, id_number, (lathe_col,), (cleared_or_not,))

def update_machine(id_number, cleared_or_not):
    db.update_entry(db_name, tb_name, id_col, id_number, (machine_col,), (cleared_or_not,))

# clearances is a list of 0 or 1s for machine, mill, and lathe
def add_person(id_number, name, clearances):
    # db columns
    cols = ('name', id_col, machine_col, mill_col, lathe_col)
    val_list = tuple([name, id_number] + clearances)
    db.insert_entry(db_name, tb_name, cols, val_list)

def remove_person(id_number):
    db.remove_entry(db_name, tb_name, id_col, (id_number,))

def view_db():
    db.get_table_info(db_name, tb_name)

# def power_on(relay):
#     # assuming it latches
#     GPIO.output(relay, GPIO.HIGH)


# def power_off(relay):
#     GPIO.output(relay, GPIO.LOW)

# # Capture SIGINT for cleanup when the script is aborted
# def end_read(signal, frame):
#     global continue_reading
#     print
#     "Ctrl+C captured, ending read."
#     continue_reading = False
#     GPIO.cleanup()

# def main():
#     print("Starting up")
#     db = "" #insert name here
#     conn = sqlite3.connect(db)
#     c = conn.cursor()
#     relay = 0 #pick a pin, any pin
#     GPIO.setup(relay, GPIO.output)
#     column_list = c.execute("PRAGMA table_info{db}".format(db = db)).fetchall()
#     table_name = str(c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchone())
#     # adjust as necessary
#     column_name = column_list[0]
#     id_column = column_list[1]

#     # Hook the SIGINT
#     signal.signal(signal.SIGINT, end_read)

#     # Create an object of the class MFRC522
#     MIFAREReader = MFRC522.MFRC522()

#     # Gotta figure out what to do about this loop
#     # This loop keeps checking for chips. If one is near it will get the UID and authenticate
#     print("Start")
#     debounce = 0
#     while continue_reading:

#         # Scan for cards
#         (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

#         # Get the UID of the card
#         (status, uid) = MIFAREReader.MFRC522_Anticoll()

#         # If we have the UID, continue
#         if status == MIFAREReader.MI_OK and debounce == 0:
#             id_num = 0
#             debounce = 5
#             # Print UID
#             print("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
#             for i in range(4):
#                 id_num += ((int(uid[i])) *(10 ** (3 * (3 - i))))

#             if check_clearances(id_num, c, column_name, table_name, id_column):
#                 state = not state
#                 power_on(relay) if state == 1 else power_off(relay)

#         elif debounce != 0:
#             assert(debounce > 0)
#             debounce -= 1

#         else:
#             continue

#                 # Came with the thing, looks unnecessary
#                 # # This is the default key for authentication
#                 # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

#                 # # Select the scanned tag
#                 # MIFAREReader.MFRC522_SelectTag(uid)

#                 # # Authenticate
#                 # status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

#                 # # Check if authenticated
#                 # if status == MIFAREReader.MI_OK:
#                 #     MIFAREReader.MFRC522_Read(8)
#                 #     MIFAREReader.MFRC522_StopCrypto1()
#                 # else:
#                 #     print "Authentication error"




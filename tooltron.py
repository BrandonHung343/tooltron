import sqlite3
import time
import RPi.GPIO as GPIO
import MFRC522
import signal

from sqlite3 import Error

def db_new(name, *args, **kwargs):
	if kwargs is not None:
		counter = 0
		conn = sqlite3.connect(name)
		c = conn.cursor()
		for key, value in kwargs.iteritems():
			counter += 1
			try:
				c.execute("CREATE TABLE {tn} ({nf} {ft})").format(tn=args[counter], nf=key, ft=value)
			except Error as e:
				print(e)
		print("DB created")
		conn.commit()
		conn.close()
	else:
		print("fields and types not properly created")

def check_clearances(id, c, column_name, table_name, id_column):
	c.execute("SELECT ({cn}) FROM {tn} WHERE {idf}={id}".format(cn=column_name, tn=table_name, idf=id_column, id=id))
	all_rows = c.fetchone()
	print(all_rows)
	if (all_rows is not None and all_rows[0] != 0):
		return True
	return False


def power_on():
    # assuming it latches
    GPIO.output(relay, GPIO.HIGH)


def power_off():
    GPIO.output(relay, GPIO.LOW)


# Capture SIGINT for cleanup when the script is aborted
def end_read(signal, frame):
    global continue_reading
    print
    "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

def main():
    print("Starting up")
    db = "" #insert name here
    conn = sqlite3.connect(db)
    c = conn.cursor()
    column_list = c.execute("PRAGMA table_info{db}".format(db = db)).fetchall()
    table_name = str(c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchone())
    # adjust as necessary
    column_name = column_list[0]
    id_column = column_list[1]

    # Hook the SIGINT
    signal.signal(signal.SIGINT, end_read)

    # Create an object of the class MFRC522
    MIFAREReader = MFRC522.MFRC522()

    # Gotta figure out what to do about this loop
    # This loop keeps checking for chips. If one is near it will get the UID and authenticate
    print("Start")
    debounce = 0
    while continue_reading:

        # Scan for cards
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # Get the UID of the card
        (status, uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK and debounce == 0:
            id_num = 0
            debounce = 5
            # Print UID
            print("Card read UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
            for i in range(4):
                id_num += ((int(uid[i])) *(10 ** (3 * (3 - i))))

            if check_clearances(id_num, c, column_name, table_name, id_column):
                state = not state
                power_on() if state == 1 else power_off()

        elif debounce != 0:
            assert(debounce > 0)
            debounce -= 1

        else:
            continue

                # Came with the thing, looks unnecessary
                # # This is the default key for authentication
                # key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]

                # # Select the scanned tag
                # MIFAREReader.MFRC522_SelectTag(uid)

                # # Authenticate
                # status = MIFAREReader.MFRC522_Auth(MIFAREReader.PICC_AUTHENT1A, 8, key, uid)

                # # Check if authenticated
                # if status == MIFAREReader.MI_OK:
                #     MIFAREReader.MFRC522_Read(8)
                #     MIFAREReader.MFRC522_StopCrypto1()
                # else:
                #     print "Authentication error"




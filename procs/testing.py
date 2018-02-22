import requests
import sys

url = "http://127.0.0.1:5000/index"
txtpath = "../raw_files/varlog.txt"


def read_file():
    try:
        f = open(txtpath, 'r')
        for line in f:
            send_data(line)
        f.close()
    except:
        print("Failed to open the file.")

def send_data(mydata):
    url = "http://127.0.0.1:5000/insert/here"
    try:
        # res = requests.post(url, data=mydata)
        requests.post(url=url, data=mydata)
        print("Sent data.")
    except:
        print("Failed to post to the server.")


def main():
    read_file()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()

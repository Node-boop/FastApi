#! /usr/bin/python3
import requests

def Main():
    url = "http://127.0.0.1:8000/"
    token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjQ5Njc4NDQyMzE5YTQ3YTg5MTJlMzQ3YmI2MWI5MDQ0IiwiZXhwIjoxNzQ4NjAzMjcxfQ.wI2-CYsEZl62DupfUsGR4I5ymU-wf_wz8648RLNybTM"
    r = requests.get(url + "api/v1/users")
    print(r.headers)
    print(r.json())

if __name__=='__main__':
    Main()

    


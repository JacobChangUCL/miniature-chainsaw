# This file is used to limit the login attempts of an IP address.
# written by: Jingbo Zhang,17/07/2024
import time


class IP_banning:
    """
    This class is used to limit the login attempts of an IP address.
    """
    def __init__(self, ban_time=300, ban_attempts=4):
        self.attempts = {}  # store the attempts of each IP
        self.ban_time = ban_time  # 5 minutes ban
        self.ban_attempts = ban_attempts  # after 4 attempts, ban the IP

    def check_ban(self, ip):
        """
        Check if the IP is banned
        :param ip: the ip address we want to check
        :return: True if the ip is not banned, False if the ip is banned
        """
        if ip in self.attempts:  # if it is not the first time the ip is trying to log in
            if self.attempts[ip][0] < self.ban_attempts:
                # if the attempts are less than max attempts
                self.attempts[ip][0] += 1  # add 1 to the attempts
                return True
            if self.attempts[ip][1] == 0:  # if it's first time reach the limit
                self.attempts[ip][1] = time.time() + self.ban_time  # set the ban time
            if self.attempts[ip][1] < time.time():
                # if it is not the first time reach the limit and the ban time is not over
                return False
            if self.attempts[ip][1] >= time.time():
                # if it is not the first time reach the limit and the ban time is over
                self.attempts.pop(ip)  # remove the banning
                return True
        else:  # the first time the ip is trying to log in
            self.attempts[ip] = [1, 0]
            # in [1,0], 1 is the attempts, 0 is the ban time
            # if the second element is 0, it means the ip is not banned
            # if the second element is a time, it means the ip is banned until that time
            return True

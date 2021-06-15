import random, sys, os
import mysql.connector as mysql
from . classes import User, Data

USER_PATH = "D:\\Development Environment\\data\\tripod\\Users\\"
SERVER_PATH = "D:\\Development Environment\\data\\tripod\\Pods\\"
# USER_PATH = "D:\\Development Environment\\data\\tripod\\Users\\"

class DataHandler:

    def __init__(self):

        try:
            self.serv_db = mysql.connect(host='localhost', user="root", password="root123", database="tripod")
            self.cursor = self.serv_db.cursor()
        except Exception as e:
            print("db problems")
            print(e)

    def createUser(self, user):

        uid = random.randint(1000, 9999)

        sql = """INSERT INTO USERS VALUES(%s, %s, %s, %s)"""

        if not self.verifyUser(user):
            try:
                self.cursor.execute(sql, (uid, user.name, user.email, user.pasd))
                self.serv_db.commit()
                os.mkdir(USER_PATH+str(uid))
                open(USER_PATH+str(uid)+"\\servers_file.txt", "w+")
                print(user.name, "User Added.")
                return uid
            except Exception as e:
                print(e)
                self.serv_db.rollback()
        else:
            print("User Already Exists with email :", user.email)

    def verifyUser(self, user):

        sql = """SELECT * FROM USERS WHERE email = %s"""

        try:
            self.cursor.execute(sql, (user.email,))
            output = self.cursor.fetchall()
            # print(output[0])
            if output and output[0][2] == user.email:
                return 1
            else:
                return 0
        except Exception as e:
            print("problem with fetching data")
            print(e)
            return -1

    def getName(self, id, type="user"):

        if type == "user":
            sql = """SELECT name FROM USERS WHERE uid = %s"""
        elif type == "server":
            sql = """SELECT name FROM PODS WHERE uid = %s"""

        try:
            self.cursor.execute(sql, (id,))
            output = self.cursor.fetchall()
            return output[0][0]
        except Exception as e:
            print("problem with fetching data", e)

    def UpdateUserData(self, userID, data):

        userID = str(userID)
        try:
            if data.server_file:
                with open(USER_PATH+userID+"\\servers_file.txt", "w+") as file:
                    file.write(data.server_file)

            if data.friends_file:
                with open(USER_PATH+userID+"\\friends_file.txt", "w+") as file:
                    file.write(data.friends_file)

            print("Updated.")
        except Exception as e:
            print(e)

    def CreateFriendLink(self, userA, userB):
        bname = self.getName(userB)
        aname = self.getName(userA)

        try:
            data = '['+bname+', '+userB+"] -\n"
            with open(USER_PATH+userA+"\\friends_file.txt", "a+") as file:
                file.write(data)
                file.close()

            data = '['+aname+', '+userA+"] -\n"
            with open(USER_PATH+userB+"\\friends_file.txt", "a+") as file:
                file.write(data)
                file.close()
            print("Friends Added.")
        except Exception as e:
            print("problem :", e)

    def getID(self, email):

        try:
            sql = """SELECT uid from Users where email = %s"""
            self.cursor.execute(sql, (email,))
            output = self.cursor.fetchall()
        except Exception as e:
            print("Problem while fetching\n", e)

    def verifyPod(self, podID):

        sql = """SELECT * FROM PODS WHERE uid = %s"""

        try:
            self.cursor.execute(sql, (podID,))
            output = self.cursor.fetchall()
            # print(output[0])
            if output and output[0][0] == podID:
                return 1
            else:
                return 0
        except Exception as e:
            print("problem with fetching data", e)
            return -1

    def CreatePod(self, podname, owner):


        uid = random.randint(1001, 9999)
        while self.verifyPod(uid):
            uid = random.randint(1001, 9999)

        sql = """INSERT INTO pods VALUES(%s, %s, %s)"""

        try:
            self.cursor.execute(sql, (uid, podname, owner))
            self.serv_db.commit()

            os.mkdir(SERVER_PATH+str(uid))
            os.mkdir(SERVER_PATH+str(uid)+"\\data")
            with open(SERVER_PATH+str(uid)+"\\members.txt", "w+") as file:
                file.write("["+self.getName(owner)+","+owner+"] -\n")
            with open(SERVER_PATH+str(uid)+"\\titles.txt", "w+") as file:
                file.write("[OWNER, "+owner+"] -")

            print("Pod created.")
        except Exception as e:
            self.serv_db.rollback()
            print("Error while creating pod", e)

    def CreatePodLink(self, userID, podID):

        try:
            with open(SERVER_PATH+str(podID)+"\\members.txt", "a+") as file:
                file.write("["+self.getName(userID)+","+userID+"] -")

            data = '['+self.getName(str(podID), type="server")+', '+str(podID)+"] -\n"
            with open(USER_PATH+userID+"\\servers_file.txt", "a+") as file:
                file.write(data)
                file.close()
            print(self.getName(userID), "Joined", self.getName(podID, type="server"))
        except Exception as e:
            print("Problem :", e)


class UI_Requests:

    def __init__(self, server):

        self.server = server

    def send(self, data):
        self.server.send(data)


dh = DataHandler()
data = Data()
# user.setDets("Bossman", "bruhemail@gmail.com", "bossmanjesus")
# user.setID(dh.createUser(user))
# with open("user\\self.txt", "w+") as file:
#     file.write(user.toString())

# dh.UpdateUserData(1537, data)
# user = User()
#
# with open("user\\self.txt", "r") as file:
#     out = file.read()
#     user.fromstring(out)
# dh.CreatePodLink(user.uid, 3029)
# dh.CreatePod("Pod1", user.uid)

# dh.CreateFriendLink(user.uid, str(1480))
# lis = list(data.friends_file.split(" -\n"))
# print(lis)

import click, requests, hashlib,os,time
from getpass import getpass

class appUser:
    def __init__(self, name="", username="", password="",salt=""):
        self.name = name
        self.username = username
        self.password = password
        self.salt = salt
        self.loggedIn = False
    def show(self):
        click.echo(f"Name: {self.name}\nUser ID: {self.username}\n")

userList = dict()

def extractUser():
    try:
        readFile = open("theLoggedIn.txt","r")
        line = readFile.read()
        myList = list(line.split(","))
        user = appUser(myList[0],myList[1],myList[2],myList[3])
        user.loggedIn = True
        readFile.close()
        return user
    except:
        user = appUser()
        return user

def before():
    try:
        readFile = open("theUsersList.txt","r")
        line = readFile.readline()
        while(line):
            myList = list(line.rstrip("\n").split(","))
            user = appUser(myList[0],myList[1],myList[2],myList[3])
            userList[user.username] = user
            line = readFile.readline()
        readFile.close()
    except:
        pass

def after():
    writeFile = open("theUsersList.txt","w")
    for userID in userList.keys():
        myList = []
        myList.append(userList[userID].name)
        myList.append(userList[userID].username)
        myList.append(userList[userID].password)
        myList.append(userList[userID].salt)
        writeFile.write(",".join(myList)+"\n")
    writeFile.close()
    click.echo("Application Terminated.")

masterKey = "thisismyapp"

def hashPass(passw,salt):
    passw = passw + salt + masterKey
    enc = passw.encode()
    hashed = hashlib.md5(enc).hexdigest()
    return hashed

def logIn():
    before()
    enterUserID = input("Enter your username: ")
    if(enterUserID not in userList.keys()):
        click.echo("Invalid username. Try again. ")
        return logIn()
    enterPass = getpass("Enter your password: ")
    enterPass = hashPass(enterPass,userList[enterUserID].salt)
    if(enterPass!=userList[enterUserID].password):
        click.echo("Incorrect password. Try again. ")
        return logIn()
    userList[enterUserID].loggedIn = True
    click.echo("You have successfully logged in.")
    writeFile = open("theLoggedIn.txt","w")
    myList = []
    myList.append(userList[enterUserID].name)
    myList.append(userList[enterUserID].username)
    myList.append(userList[enterUserID].password)
    myList.append(userList[enterUserID].salt)
    writeFile.write(",".join(myList)+"\n")
    writeFile.close()
    return userList[enterUserID]

def logOut():
    user = extractUser()
    user.loggedIn = False
    writeFile = open("theLoggedIn.txt","w")
    writeFile.write("")
    writeFile.close()

def register():
    os.system('cls' if os.name == 'nt' else 'clear')
    salt = str(os.urandom(16))
    enterName = input("Enter your Name:")
    if not enterName:
        click.echo("Name can not be left blank.")
        time.sleep(1)
        register()
        return
    enterUserID = input("Enter your username:")
    if not enterUserID:
        click.echo("Username can not be left blank.")
        time.sleep(1)
        register()
        return
    if(enterUserID in userList):
        click.echo("Entered username is already in use. Try again.")
        time.sleep(1)
        register()
        return
    flag = True
    while(flag):
        enterPass = getpass("Set your password:")
        confPass = getpass("Confirm your password:")
        if((enterPass==confPass) and (enterPass!="")):
            flag = False
            enterPass = hashPass(enterPass,salt)
            user = appUser(enterName,enterUserID, enterPass, salt)
            userList[enterUserID] = user
        if(flag):
            click.echo("Password did not match. Try again")
    writeFile = open("theUsersList.txt","a")
    myList = []
    myList.append(user.name)
    myList.append(user.username)
    myList.append(user.password)
    myList.append(user.salt)
    writeFile.write(",".join(myList)+"\n")
    writeFile.close()

def display(info):
    try:
        x = info['main']
        hum = x['humidity']
        press = x['pressure']
        avgTemp = x['temp']
        windSpeed = info['wind']['speed']
        windDegree = info['wind']['deg']
        click.echo(f"Humidity (in percentage) = {hum}\nAtmospheric pressure (in hPa unit) = {press}\nTemperature (in celsius) = {avgTemp - 273.15}\nWind Speed = {windSpeed}\nWind Degree = {windDegree}")
    except KeyError:
        click.echo("Information unavailable.")

@click.command(help="Use it find the weather")
def weather():
    user = extractUser()
    if(user.loggedIn!=True):
        click.echo("You're not allowed to use this feature. You need to log in first.")
        user = logIn()
    makeAPIcall()

def makeAPIcall():
    os.system('cls' if os.name == 'nt' else 'clear')
    dateList = dict()
    click.echo("Choose one of the two formats(for location):\n1. Name of the city\n2. Latitude and Longitude\n3. Quit")
    ch = 0
    try:
        ch = int(input("Your choice:"))
    except ValueError:
        click.echo("Please enter an appropiate choice.")
        makeAPIcall()
        return
    baseUrl = "http://api.openweathermap.org/data/2.5/weather?"
    apiKey = "e12c5165e1c9c0996e906b8eaad83cfd"
    if(ch==1):
        cityName = ""
        while(cityName==""):
            cityName = input("Enter city name : ")
            if(cityName!=""):
                break
        url = f"{baseUrl}appid={apiKey}&q={cityName}"
        try:
            response = requests.get(url)
        except:
            click.echo("Something went wrong.")
            click.echo("Try checking your internet connection.")
            input("Click Enter to exit.")
            return
        jsonFile = response.json()
        if (jsonFile['cod'] != "404"):
            lat = jsonFile["coord"]["lat"]
            lon = jsonFile["coord"]["lon"]
        else:
            click.echo("City not found.")
            return
    elif(ch==2):
        flag = True
        while(flag):
            lat = float(input("Enter the latitude of the location(in range of -90 deg to 90 deg): "))
            lon = float(input("Enter the longitude of the location(in range of -180 deg to 180 deg): "))
            if((lat>-90 and lat<90) and (lon>-180 and lon<180)):
                flag = False
            if(flag):
                click.echo("Please enter the values in appropriate range.")
    elif(ch==3):
        return
    else:
        click.echo("Please enter an appropiate choice.")
        time.sleep(1)
        makeAPIcall()
        return

    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={apiKey}"
    try:
        response = requests.get(url)
    except:
        click.echo("Something went wrong.")
        click.echo("Try checking your internet connection")
        input("Click Enter to exit.")
        return
    jsonFile = response.json()
    if (jsonFile['cod'] != "404"):
        x = jsonFile["list"]
        for i in range(40):
            dt,t = x[i]['dt_txt'].split(" ")
            if(dt not in dateList):
                dateList[dt] = dict()
            dateList[dt][t] = x[i]
        listOfDates = []
        i = 1
        click.echo("Choose among the following dates:")
        for dateKey in dateList.keys():
            click.echo(f"{i}. {dateKey}")
            listOfDates.append(dateKey)
            i+=1
        click.echo()
        chOfDate = -1
        flag = True 
        while(flag):
            try:
                chOfDate = int(input("Your choice:"))
                flag = False
            except ValueError:
                click.echo("Please enter an appropiate choice.")
                flag = True
            if(chOfDate not in range(1,i)):
                flag = True
                click.echo("Invalid choice. Choose again.")
            flag = False

        chOfDate-=1
        listOfTimes = []
        i = 1
        flag = True 
        chOfTime = -1
        click.echo("Choose among the following time slots:")
        for timeKey in dateList[listOfDates[chOfDate]].keys():
            click.echo(f"{i}. {timeKey}")
            listOfTimes.append(timeKey)
            i+=1
        while(flag):
            try:
                chOfTime = int(input("Your choice:"))
                flag = False
            except ValueError:
                click.echo("Please enter an appropiate choice.")
                flag = True
            if(chOfTime not in range(1,i)):
                flag = True
                click.echo("Invalid choice. Choose again.")
            flag = False

        chOfTime-=1
        if(jsonFile['city']['name']!=""):
            click.echo(f"Name of the city: {jsonFile['city']['name']}")
        display(dateList[listOfDates[chOfDate]][listOfTimes[chOfTime]])
    else:
        click.echo("City not found.")
    click.echo("Click Enter to exit")
    input()

def updateUserID(user):
    userID = input("Enter your new Username:")
    if(userID in userList.keys()):
        click.echo("Username already in use. Try another one.")
        updateUserID(user)
        return
    del userList[user.username]
    user.username = userID
    userList[userID] = user

def updatePass(user):
    userID = user.username
    oldPass = getpass("Enter old password: ")
    if(hashPass(oldPass,userList[userID].salt)!=userList[userID].password):
        click.echo("Password didn't match. Try again.")
        updatePass(user)
        return
    flag = True
    while(flag):
        newPass = getpass("Enter new password: ")
        confnewPass = getpass("Enter new password again: ")
        if(newPass==confnewPass):
            userList[userID].password = hashPass(newPass,userList[userID].salt)
            flag = False
        if(flag):
            click.echo("Password didn't match. Try again")

def updateInfo(user):
    os.system('cls' if os.name == 'nt' else 'clear')
    ch = 0
    try:
        ch = int(input("What do you want to update?\n1. Name\n2. Username\n3. Password\n4. Quit.\nYour choice: "))
    except ValueError:
        click.echo("Please enter an appropiate choice.")
        updateInfo(user)
        return
    if(ch == 1):
        name = input("Enter your new name:")
        userID = user.username
        userList[userID].name = name
        click.echo(f"You have successfully changed your name to {userList[userID].name}.")
    elif(ch==2):
        updateUserID(user)
        click.echo(f"You have successfully changed your username to {user.username}.")
    elif(ch==3):
        updatePass(user)
        click.echo(f"You have successfully changed your password.")
    elif(ch==4):
        return
    else:
        click.echo("Invalid choice.")
    click.echo("Click Enter to exit")
    input()

def printAllUsers():
    for userID in userList.keys():
        userList[userID].show()
    click.echo("Click Enter to exit")
    input()

def delUser(user):
    ch = input("Are you sure you want to delete your account?(y/n): ")
    if(ch=='y' or ch=='Y'):
        try:
            del userList[user.username]
            logOut()
            click.echo("You have deleted your account.")
            after()
        except:
            click.echo("User doesn't exist.")
    elif((ch=='n' or ch=='N')):
        return
    else:
        click.echo("Inavlid choice.")
        delUser(user)

def menu(user):
    if(user.loggedIn!=True):
        click.echo("You're not logged in.")
        return
    ch = 0 
    while(ch!=4 and ch!=5):
        click.echo("What would you like to do?\n1. Check weather information for scheduled flight.\n2. Update user information.\n3. Read all users' information\n4. Delete user\n5. Log out\n6. Quit")
        ch = 0
        flag = True
        while(flag):
            try:
                ch=int(input("Your choice:"))
                flag = False
            except ValueError:
                click.echo("Please enter an appropiate choice.")
        if(ch==1):
            makeAPIcall()
        elif(ch==2):
            updateInfo(user)
        elif(ch==3):
            printAllUsers()
        elif(ch==4):
            delUser(user)
            time.sleep(2)
        elif(ch==5):
            logOut()
            click.echo("You have successfully logged out.")
            return
        elif(ch==6):
            return
        else:
            click.echo("Invalid choice")
            time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
    after()

def main():
    user = extractUser()
    if(user.loggedIn==True):
        menu(user)
    click.echo("Choose from the following:\n1. Log In\n2. Sign Up\n3. Quit")
    c = 0 
    try:
        c = int(input("Your choice:"))
    except ValueError:
        click.echo("Please enter an appropiate choice.")
        main()
        return
    if(c==1):
        user = logIn()
        click.echo(f"Hello {user.name}")
    elif(c==2):
        register()
        click.echo("You have successfully registered. To use your account you'll have to log in first.")
        main()
        return
    elif(c==3):
        return
    else:
        click.echo("Invalid choice")
    os.system('cls' if os.name == 'nt' else 'clear')
    menu(user)

@click.group()
def entry():
    pass

@click.command(help="Use to execute the application.")
def run():
    os.system('cls' if os.name == 'nt' else 'clear')
    before()
    main()
    after()

@click.command(help="Use to login to the application.")
def login():
    before()
    user = extractUser()
    if(user.loggedIn==True):
        click.echo(f"Hey {user.name} you're already logged in.")
        menu(user)
    user = logIn()
    click.echo(f"Hello {user.name}")
    after()


@click.command(help="Use to register with the application.")
def reg():
    register()
    click.echo("You have successfully registered. You can continue after logging In.")

@click.command(help="Look at all the available features.")
def Menu():
    before()
    user = extractUser()
    if(user.loggedIn==True):
        menu(user)
    else:
        click.echo("You need to login first.")
    after()

@click.command(help="Update your profile information.")
def update():
    before()
    user = extractUser()
    if(user.loggedIn==True):
        updateInfo(user)
    else:
        click.echo("You need to login first.")
    after()


@click.command(help="Use to logout to the application.")
def logout():
    user = extractUser()
    if(user.loggedIn!=True):
        click.echo("You're not logged in.")
    else:
        logOut()
        click.echo("You have successfully logged out.")

entry.add_command(login)
entry.add_command(run)
entry.add_command(reg)
entry.add_command(weather)
entry.add_command(logout)
entry.add_command(Menu)
entry.add_command(update)
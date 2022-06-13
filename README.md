# CLI Application - Weather extraction

It is a Command line interface application. Use this to find out the weather from today till 5 days at any specified time, to know the weather before your flight takes off.

## How to install

1. `git clone https://github.com/samanvipotnuru/cliapp-weather.git`
2. `cd myapp`
3. `pip install .`
4. `myapp [cmd]`

[cmd] - You can use all the commands that have been explained below.

```c
Usage: myapp [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  login    Use to login to the application.
  logout   Use to logout to the application.
  menu     Look at all the available features.
  reg      Use to register with the application.
  run      Use to execute the application.
  update   Update your profile information.
  weather  Use it find the weather
```

## Available Commands for the CLI

### 1. reg

```
myapp reg
```

Register with the application using 'reg' command, enter your details, create a username and set your password. After registering you can continue using the application once you login.

### 2. login

```
myapp login
```

Provide your set username and password to login to the application. You won't be able to use the other features of the application without logging in first.

### 3. logout

```
myapp logout
```

Run this command if you want to logout of the application.

### 4. menu

```
myapp menu
```

This command will show you all available functions, you can choose to perform any action you want. But you need to login first.

### 5. update

```
myapp update
```

This command lets you update your user details such as username and password etc. But you need to login first.

### 6. weather

```
myapp weather
```

This command lets you check the weather of any particular location at specified time from today till 5 days. But you need to login first.

### 7. run

```
myapp run
```

This command runs the application from the beginning to the end, with all features being usable.

## Testing

A unit test named 'test_cli.py' is available to run tests for important methods in this application.

Go to the directory the files are saved in.

```
python -m unittest test_cli.py
```

Run the above command on the terminal to run the unit tests.

## API

The [openweathermap api](https://openweathermap.org/api) was used to extract the weather information. Further details regarding the api are availble at their website.

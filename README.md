
# Audience Real Time Questions with Moderation


Users can put their questions, and all their questions go to the moderator, and the moderator can filter out genuine inquiries, which then move to a public endpoint. All this process happens in real-time(using WebSockets).






## Tech Stack

**Client:** HTML, CSS, JavaScript

**Server:** Python, Django, Django Channels

**Database:** SQLite


  
## Run Locally


Clone the project

```bash
  git clone https://github.com/creative-computing-society/placement-talks.git
```

Go to the project directory

```bash
  cd placement-talks
```

We recommend you to use virtual environment

```bash
  python -m venv env
```

Activate virtual environment   
For Windows PowerShell
```bash
    env/Scripts/activate.ps1
```
For Linux and MacOS
```bash
    source env/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Install *redis*

Add *Security Key* : Go to project's *settings.py* file and change the value of *SECURITY_KEY* variable to desired security key.

Run Migrations

```
 python manage.py makemigrations
```
```
 python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```



  
## Team

* [Aditya Parmar](https://github.com/adityaParmar9813)
* [Tijil Malhotra](https://github.com/TijilM)
* [Arvinder Singh Kandola](https://github.com/askandola)

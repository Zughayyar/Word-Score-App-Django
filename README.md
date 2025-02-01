# Word Score Web App

## 📌 Project Overview
This project is a Django-based web application that allows users to analyze the occurrence of a specific word across multiple pages starting from a given URL. The application utilizes Celery and Redis for asynchronous processing to prevent long response times.

This README provides an overview of how to handle real-world challenges, explains why the application is I/O bound, and outlines strategies for scaling the application in a distributed environment.


## ⚙️ Tech Stack
- **Backend:** Django, Celery
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (Not used at this stage)

## Requirements

- [uv](https://docs.astral.sh/uv): A tool used to manage the environment for this project.
- [redis](https://redis.io/): An open source, in-memory, NoSQL key/value store
  ```sh
      brew install redis  # macOS
      apt install redis   # Linux
  ```

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository

```sh
    git clone https://github.com/Zughayyar/Word-Score-App-Django.git
```

### 2️⃣ Navigate to the project directory

```sh
    cd Word-Score-App-Django
```

### 3️⃣ Install Dependencies
```sh
    pip install -r requirements.txt
```

### 4️⃣ Configure Redis (Ensure Redis is Running)
```sh
    redis-cli ping  # Should return 'PONG'
```
If Redis is not running:
```sh
    sudo systemctl start redis  # Linux
    brew services start redis   # macOS
```

### 5️⃣ Apply Migrations & Create a Superuser
```sh
    python manage.py migrate
    python manage.py createsuperuser
```

### 6️⃣ Start the Django Server
```sh
    python manage.py runserver
```

### 7️⃣ Start Celery Worker
```sh
    celery -A _word_score worker --loglevel=info
```

### 8️⃣ Start Celery Beat (Optional, for Periodic Tasks)
```sh
    celery -A _word_score beat --loglevel=info
```

---

## 📌 How It Works
1. **User Inputs** a URL and a word.
2. The application **fetches** all linked pages up to a certain depth.
3. It **counts** the word occurrences asynchronously using Celery.
4. Results are **stored in the session** and users are redirected to the homepage to view the results.


## 📞 Contact
- **Author:** Anas Zughayyar  
- **Email:** anas.ezzughayyar@gmail.com  
- **LinkedIn:** [linkedin.com/in/anasez](https://www.linkedin.com/in/anasez)


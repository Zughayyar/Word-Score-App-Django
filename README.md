# Word Score Web App

## 📌 Project Overview
This project is a Django-based web application that allows users to analyze the occurrence of a specific word across multiple pages starting from a given URL. The application utilizes Celery and Redis for asynchronous processing to prevent long response times.

---

## ⚙️ Tech Stack
- **Backend:** Django, Celery
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite (default, can be switched to PostgreSQL/MySQL)
- **Task Queue:** Celery
- **Message Broker:** Redis

---

## 🚀 Setup & Installation

### 1️⃣ Clone the Repository
```sh
    git clone https://github.com/yourusername/word-score.git
    cd word-score
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
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

---

## 🛠 Environment Variables
Ensure you configure the `.env` file properly (if needed) with:
```ini
SECRET_KEY=your_django_secret_key
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
```

---

## 🔥 API Endpoints
| Method | Endpoint        | Description                     |
|--------|----------------|---------------------------------|
| POST   | `/word-score/` | Submits a URL and word to analyze |
| GET    | `/`            | Displays the results page |

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🤝 Contributing
Feel free to contribute by opening an issue or a pull request!

---

## 📞 Contact
- **Author:** Anas Zughayyar  
- **Email:** anas.ezzughayyar@gmail.com  
- **LinkedIn:** [linkedin.com/in/anasez](https://www.linkedin.com/in/anasez)

---

⭐️ If you find this project useful, consider giving it a star on GitHub! 🚀


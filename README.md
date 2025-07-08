![Screenshot (140)](https://github.com/user-attachments/assets/e3485865-cd5e-4fbe-af38-b22f217f6c0d)
![Screenshot (141)](https://github.com/user-attachments/assets/85d6b5f7-8fe4-4f67-b79e-1485353c9d17)
![Screenshot (144)](https://github.com/user-attachments/assets/c1c000e6-d378-40c2-b27b-c77933256b2f)
![Screenshot (145)](https://github.com/user-attachments/assets/fee1bc63-e578-4955-bd79-9148de9db3c6)
# 📝 Django Real-Time Blog

A feature-rich blog application built using **Django** and **Django Channels**, supporting real-time notifications, user interactions, profile management, and a clean Bootstrap frontend.

---

## 🚀 Features

- ✍️ Create, edit, and delete blog posts  
- 🖼️ Upload post images  
- 💬 Comment system with moderation  
- ❤️ Like system (posts & comments, powered by GenericForeignKey)  
- 👤 User profiles with:
  - Bio, profile picture, age, website, location
  - Follow/Unfollow and Block/Unblock logic
- 🔔 Real-time notifications (WebSocket + Channels)
- 📡 WebSocket powered by **Daphne**
- 💡 Tip of the Day from ZenQuotes API
- 🧪 Signals trigger notifications on:
  - New post by someone you follow
  - Like on your post/comment
  - Comment on your post

---

## 🧠 Data Models

### `BlogPost`
- `title`, `slug`, `content`, `image`, `author`, `likes`
- Ordered by `created_at DESC`
- Linked to `Like` via `GenericRelation`

### `Comment`
- Belongs to a `BlogPost` and `User`
- Includes `approved` flag
- Also supports `Like` via GenericRelation

### `Like`
- A **generic like model** that supports any content type (post, comment, etc.)
- Ensures unique (user + content) likes

### `Profile`
- One-to-One with `User`
- Fields: `bio`, `profile_pic`, `website`, `location`, `joined_at`, etc.
- Includes:
  - ✅ Follow/Unfollow logic
  - 🚫 Block/Unblock logic
  - 👥 Tracks followers and following relationships

---

## 🔔 Real-Time Notifications

Django signals trigger `send_notification_to_user(user_id, message)` when:

- A user you follow creates a post
- Someone likes your post
- Someone likes your comment
- Someone comments on your post

These are sent live using WebSockets (`ws://`) and appear in your notification panel.

---

## ⚙️ Tech Stack

- **Backend**: Django 4+, Channels, Daphne
- **Frontend**: Bootstrap 5
- **Database**: SQLite (can use PostgreSQL for prod)
- **Media Handling**: `MEDIA_URL` + `MEDIA_ROOT`
- **Live Events**: WebSockets (Daphne + Channels)
- **API**: `ZenQuotes` (for tips)
- **Dev Tools**: Django admin, VS Code, Git

---

## 🧪 Setup Instructions

### 1. Clone the repository

```bash
python -m virtualenv venv
venv\Scripts\activate # for Windows
source venv/bin/activate    # For mac or other
git clone https://github.com/rayyan22207/Blog.git
cd src
python manage.py migrate
python manage.py createsuperuser
daphne core.asgi:application



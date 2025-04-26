# Nano-URL : Secure URL Shortener

A secure, email-verified URL shortener built with **FastAPI** and **Supabase PostgreSQL**.

🌐 [Live Demo](https://nano-url-production.up.railway.app/)

---

## ✨ Features

- **Email-based access control**: Only authorized users can access shortened URLs.
- **JWT verification**: Access tokens are sent via email and expire after 24 hours.
- **Creator notifications**: URL creators receive email alerts when someone accesses their links.
- **Token expiration & rate-limiting**: Secure handling of token timeouts and abuse prevention.
- **Deployed on Railway**: Production-ready deployment with a smooth backend experience.

---

## 📸 How It Works

1. The creator submits an original URL to generate a shortened URL and optionally lists authorized email addresses who can access it.
2. A user who wants to access the short URL submits their email address.
3. If the email is authorized, they receive a **verification link** via email.
4. The user clicks the verification link, which verifies their identity and grants them temporary access.
5. Upon successful verification, the original URL opens, and the creator receives an email notification about the access.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: Supabase PostgreSQL
- **Authentication**: JSON Web Tokens (JWT)
- **Email**: SMTP
- **Deployment**: Railway

---

## 📬 Feedback

Feel free to [open an issue](https://github.com/Gautam413/nano-url/issues) .

---

## 📄 License

MIT License

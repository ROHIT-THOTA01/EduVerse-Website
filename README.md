#Udemy-Clone-Django

Udemy Clone Website

The site structure is not fully completed yet!

The website is still under development.

But for now, you can try it!
To run the project:
```
**Step 1:**
git clone https://github.com/Xusanbek0071/Django-Corsera-clone.git
```

**Step 2:**
```
python manage.py makemigrations
```

**Step 3:**
```
python manage.py migrate
```

**Step 4:**
```
python manage.py runserver
```

**Step 5:**
```
http://127.0.0.1:8000/
```
Technologies Used:
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
You can review the project:

Feel free to contact me if you have any suggestions or feedback.

<div align="left">
  <a href="https://t.me/mbin_dev_0071" target="_blank">
    <img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/telegram/default.svg" width="52" height="40" alt="linkedin logo"  />
  </a>
    <a href="https://instagram.com/husanbek_dev" target="_blank">
    <img src="https://raw.githubusercontent.com/maurodesouza/profile-readme-generator/master/src/assets/icons/social/instagram/default.svg" width="52" height="40" alt="linkedin logo"  />
  </a>
  
</div>

## Deploying to Render

This repository now ships with infrastructure files for the [Render](https://render.com) platform (`render.yaml`, `Procfile`, and `requirements.txt`). To deploy:

1. Push your code to GitHub (already done in this repo).
2. In Render:
   - Click **New +** → **Blueprint** → point Render to this repository. Render will read `render.yaml` and provision a PostgreSQL database plus the web service automatically.
3. Set the following environment variables in Render (Render will prompt you):

   | Variable | Purpose |
   | --- | --- |
   | `SECRET_KEY` | Django secret key (use a random 50+ char string) |
   | `DEBUG` | Set to `False` in production |
   | `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` | Comma-separated host/origin list (Render sets defaults, edit when custom domain is added) |
   | `STRIPE_PUBLISHABLE_KEY` / `STRIPE_SECRET_KEY` | Your Stripe credentials |

4. Render runs `pip install -r requirements.txt && python manage.py collectstatic --noinput` during build and `python manage.py migrate` before each deploy. The web process uses `gunicorn Coursera.wsgi --log-file -`.
5. After the first deploy finishes you can create a superuser by opening the Render shell or running `python manage.py createsuperuser` locally and connecting to the Render database.

You can still deploy elsewhere (Railway, Fly.io, etc.); Docker/WSGI friendly settings such as environment-based configuration and WhiteNoise static serving are now enabled.
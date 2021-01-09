# Flask-Blog_Posting_Website
Hello guys. I have created blog posting website in Flask framework. In which writers can post a blog with images and readers can read it from anywhere.
I would like to specially thank you Traversy Media YouTube Channel. Link: https://www.youtube.com/user/TechGuyWeb

I extend this project as per my knowledge.
New Features:
  Admin login
  Writer can upload Image or manipulate text in more ways.
  
 I have used CKEditor to upload and display images. 
 
 How to use:
  Download all files in a root directory.
  I used flask version 1.1.2.
  Configure <app.configure> section as per requirement in order to make connection with your database
  I used XAMPP for mysql.
  Change the post of MySQL to 3305.
  All CSS and JavaScript are online factable. 
  Table's Descriptions:
  
   MySQLDB [flaskapp]> DESC users;
  +---------------+--------------+------+-----+---------------------+----------------+
  | Field         | Type         | Null | Key | Default             | Extra          |
  +---------------+--------------+------+-----+---------------------+----------------+
  | id            | int(11)      | NO   | PRI | NULL                | auto_increment |
  | name          | varchar(100) | YES  |     | NULL                |                |
  | email         | varchar(100) | YES  |     | NULL                |                |
  | username      | varchar(30)  | YES  |     | NULL                |                |
  | password      | varchar(150) | YES  |     | NULL                |                |
  | register_date | timestamp    | NO   |     | current_timestamp() |                |
  | role          | varchar(50)  | YES  |     | NULL                |                |
  +---------------+--------------+------+-----+---------------------+----------------+
  7 rows in set (0.057 sec)

  MySQLDB [flaskapp]> DESC articles;
  +-------------+--------------+------+-----+---------------------+----------------+
  | Field       | Type         | Null | Key | Default             | Extra          |
  +-------------+--------------+------+-----+---------------------+----------------+
  | id          | int(11)      | NO   | PRI | NULL                | auto_increment |
  | title       | varchar(255) | YES  |     | NULL                |                |
  | author      | varchar(100) | YES  |     | NULL                |                |
  | body        | text         | YES  |     | NULL                |                |
  | create_date | timestamp    | NO   |     | current_timestamp() |                |
  +-------------+--------------+------+-----+---------------------+----------------+
  5 rows in set (0.015 sec)
  
  Thank You.

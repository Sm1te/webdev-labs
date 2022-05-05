-- Exercise 1 (done for you):
SELECT * FROM users;



-- Exercise 2 (done for you):
SELECT id, first_name, last_name 
FROM users;



-- Exercise 3
SELECT id, first_name, last_name 
FROM users 
ORDER BY last_name;



-- Exercise 4
SELECT id, image_url, user_id 
FROM posts 
WHERE user_id = 26;



-- Exercise 5
SELECT id, image_url, user_id 
FROM posts 
WHERE user_id = 26 OR user_id = 12;



-- Exercise 6
SELECT count(id) FROM posts;



-- Exercise 7
SELECT user_id, count(user_id) 
FROM comments 
GROUP BY user_id 
ORDER BY count(user_id) DESC;



-- Exercise 8
SELECT p.id, p.image_url, p.user_id, u.username, u.first_name, u.last_name
FROM users u
INNER JOIN posts p
ON (p.user_id = u.id) 
AND (p.user_id = 26 OR p.user_id = 12) ;



-- Exercise 9
SELECT p.id, p.pub_date, following_id
FROM posts p
INNER JOIN following f
ON p.user_id = f.following_id
AND f.user_id = 26;




-- Exercise 10
SELECT p.id, p.pub_date, f.following_id, u.username
FROM posts p
INNER JOIN following f
ON p.user_id = f.following_id
AND f.user_id = 26
INNER JOIN users u
ON p.user_id = u.id
ORDER BY p.pub_date DESC;



-- Exercise 11
INSERT INTO bookmarks (user_id,post_id) 
VALUES (26, 219);
INSERT INTO bookmarks (user_id,post_id) 
VALUES (26, 220);
INSERT INTO bookmarks (user_id,post_id) 
VALUES (26, 221);



-- Exercise 12
DELETE FROM bookmarks 
WHERE user_id=26 
AND post_id=219;

DELETE FROM bookmarks 
WHERE user_id=26 
AND post_id=220;

DELETE FROM bookmarks 
WHERE user_id=26 
AND post_id=221;



-- Exercise 13
UPDATE users
SET email = 'knick2022@gmail.com'
WHERE id = 26



-- Exercise 14
SELECT p.id, u.id, count(c.text), p.caption
FROM users u
INNER JOIN posts p 
ON (u.id = p.user_id)
AND u.id = 26
INNER JOIN comments c
ON (u.id = c.user_id)
AND u.id = 26
GROUP BY p.id, u.id
ORDER BY p.id;
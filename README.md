# FindMeBot
*Chatbot for Groupme, using Microsoft Cognitive Services to tag users in posted photos*

### Setting up:
Create a heroku instance, with Postgres installed

Create a table with the schema:
```
CREATE TABLE userimage (
  id INT NOT NULL,
  image BYTEA)
  ;
```
Deploy to heroku using git

Alternatively, set up a local heroku server, and configure the heroku env file to run the app locally

### Chatbot Instructions:
Post a photo, along with "this is me", to store an image for yourself

Post any photo, and the bot will repond with the nickname of the identified user

### Contributor Guide
Check out the [Contributors Guide](https://github.com/ProPorygon/FindMeBot/blob/master/contributing.md)

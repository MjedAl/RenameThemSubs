# Rename Them Subs

- A fork of [eshaan7/RenameThemSubs](https://github.com/eshaan7/RenameThemSubs) that suits my needs.  
-- Removed the PMA stuff as I only intend for this to be used locally.  
-- Subtitles now gets converted to UTF8 and the language extension is added to them.  
 
## How I use it

1. Build the app using docker `docker build . -t renamesubs`.
2. Run it with `docker run -p 1234:5000 --detach --restart=always renamesubs`.
3. Go to `localhost:1234`

### TODOs
- Take the language extension from as in input from user.
- Add the ability the select the wanted season as sometimes you would have a folder containing all the episodes for all seasons and you want to convert the subs for a specific season only.
- Refactor some part of the code.
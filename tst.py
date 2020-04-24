from database import db

def add_character(session):
    cname = input("Character name: ")
    calive = 1
    clevel = 1
    cexperience = 1

    uname = input("Username: ")
    udiscord = input("Discord ID: ")
    utype = 1
    session.add_all([
        db.User(name=uname, discord_id=udiscord, user_type_id=utype),
        db.Character(name= cname, alive = calive, level = clevel, experience = cexperience)
    ])

db.preload(db.session, db.Base)
add_character(db.session)
for ch in db.session.query(db.Character).all():
    print(ch)

#https://docs.sqlalchemy.org/en/13/orm/tutorial.html#querying-with-joins
#https://docs.sqlalchemy.org/en/13/core/metadata.html
#https://github.com/Naatoo/pygame-RPG2d/tree/develop/src/database
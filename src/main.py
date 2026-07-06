from data.build_db import DataBase

db = DataBase("assignments.db")
db.load("data/assignments.csv")
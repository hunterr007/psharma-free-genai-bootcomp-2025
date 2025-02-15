from flask import Flask
from app import create_app, db
from app.seeds.seeder import seed_data
import click

app = create_app()

@app.cli.command("create-db")
def create_db():
    """Creates the database tables."""
    db.create_all()
    print("Database tables created!")

@app.cli.command("drop-db")
def drop_db():
    """Drops the database tables."""
    db.drop_all()
    print("Database tables dropped!")

@app.cli.command("seed-db")
def seed_db():
    """Seeds the database with sample data."""
    seed_data()

if __name__ == '__main__':
    app.run()

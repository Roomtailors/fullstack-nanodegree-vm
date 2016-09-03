# Udacity Multiuser Blog Project

This project represents basic web usage aspects: Creation of accounts, simple rights management, submitting forms 

## Table of contents

* [Quick start](#quick-start)
* [Requirements](#requirements)
* [Project Structure](#project-structure)
* [License](#license)


## Quick start

1. Clone repository:
```
git clone https://github.com/Roomtailors/udacity_tournament.git
```

2. Start Vagrant 
```
vagrant up
```

3. SSH into Vagrant
```
vagrant ssh
```

4. Navigate to root/vagrant/tournament
5. Create database and tables
```
psql -f tournament.sql
```

6. Run unit tests

```
python tournament_test.py
```

## Requirements

1. Project-based Vagrant environment

Besides the project-based vagrant file no further dependencies are required. 

## Project Structure

/tournament.py  Endpoints for database operations

/tournament.sql Schema file to create database

/tournament_test.py Unchanged test file

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

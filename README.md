# MediTrack System Server

## Installation

### 1. Clone the repository:
```
git clone https://github.com/Ashani-Sansala/MediTrack_System_Backend.git
```
```
cd MediTrack_System_Backend
```
### 2. Database Initialization:

This MySQL utility allows you to store authentication credentials securely.
Run these commands once. Here's how to do it:
- Open a command prompt or terminal.
- Run the following command:
- Replace 'your_username' with your actual MySQL username.
- You'll be prompted to enter your MySQL password. Type it and press Enter.
- This creates an encrypted file (usually .mylogin.cnf in your home directory) with your credentials.
```
mysql_config_editor set --login-path=local --host=localhost --user=your_username --password
```

## Running the Server
To start the server, run:
```
python app.py
```

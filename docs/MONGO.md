MongoDB Installation and Configuration
This guide provides step-by-step instructions for installing and configuring MongoDB for the Flask me&мася App.

### 1. Install MongoDB
Follow these steps to install MongoDB on your system:

Linux:
```bash
sudo apt-get update
sudo apt-get install -y mongodb >log
```

### 2. Start MongoDB
Linux:
```bash
sudo service mongod start
```

3. Access MongoDB Shell
Open a new terminal or Command Prompt window and run:
```bash
mongo
```
### 4. Create a Database and User
In the MongoDB shell, execute the following commands:
```javascript
use pets_database
db.createUser({
  user: "admin",
  pwd: "admin",
  roles: ["readWrite", "dbAdmin"]
})
```
Replace "your_username" and "your_password" with your desired credentials.

### 5. Update Flask Application Configuration
Open the app.py file and update the MongoDB connection string:

```python
app.config['MONGO_URI'] = 'mongodb://admin:admin@localhost:27017/pets_database'
```
Replace "your_username" and "your_password" with your MongoDB credentials.

[Возврат на главную](../README.md)
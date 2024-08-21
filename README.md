# 🔃 Change Data Capture (CDC) using Logical Replication in PostgreSQL

Pre-requesites:
- Copy .env.example and set your credentials for the databases.
- Docker Desktop

## 📝 Considerations:

- You need PKs.
- INSERT, UPDATE, DELETE, TRUNCATE work good.
It doesn’t replicate the schema or DDL nor sequences.
- If you have ALL TABLES included in your publication and you create a table, you need to also to it on the target database. Otherwise it will just ignore it. 
- Schema changes are ignored. Adding or dropping columns will do nothing. Afterwards the replication will be broken.

To run the project, you can do: 

```sh
make build
NUM_RECORDS=10000 make run #Default to 5000 if not specified
```

## 🚀 Start CDC:
Docker will start by default with the wal_level set as 'logical'

```sh 
make cdc-logical-replication
```

## 🔃 Make changes:

```sh 
NUM_RECORDS=50 make insert-data 
NUM_RECORDS=50 make delete-data
NUM_RECORDS=50 make update-data
make truncate
```

Or you can run the commands yourself if you prefer.

## ✅ Check (Source):

```sql
select * from pg_publication_tables;
select * from pg_replication_slots;
```

## ✅ Check (Target):

```sql
select * from pg_subscription;

-- Overall table
select * from products;
select * from user_profiles up ;
select * from transactions t ;

-- Count rows 
select count(*) from products;
select count(*) from user_profiles up ;
select count(*) from transactions t ;

-- Check updates, inserts
select max(updated_at) from products;
select max(updated_at) from user_profiles up ;
select max(updated_at) from transactions t ;
```

## 🔨 Break the replication: 

Note: You might want to run make clean, make build and make run to restart the project if you want to keep testing.

```sh
make create-table # will be ignored, replication can continue)
make drop-table # breaks the replication if it was included in the publication, if not it will go on.
make add-column # same as drop-table
```

### 😎 [Follow me on Linkedin](https://www.linkedin.com/in/alejandro-aboy/)
- Get tips, learnings and tricks for your Data career!

### 📩 [Subscribe to The Pipe & The Line](https://thepipeandtheline.substack.com/?utm_source=github&utm_medium=referral)
- Join the Substack newsletter to get similar content to this one and more to improve your Data career!
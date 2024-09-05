# 🔃 Change Data Capture (CDC) using Logical Replication in PostgreSQL

Are you exploring CDC open-source solutions or just interested on checking how it works❓

This repo is a portable sample project for running CDC with Logical Replication. In just a few commands you can test the capabilities of this built-in Postgres features and extend it as you please.

You can find pre-made scripts to run inserts, deletes and updates just by passing `NUM_RECORDS` env var to the `make` commands. Whenever you use that command, it will randomize the amount of actions between 1 and your number.

### 🙋🏻‍♂️ Pre-requesites:
- Rename `.env.example` file to `.env` and set your credentials for the databases.
- Docker Desktop

## 📝 Considerations:

- You need PRIMARY KEYs on the TABLES you want to replicate. Not views.
- By default, it will do a full snapshot or the current table. You can disable this by using `copy_data=false` in [`cdc_logical_replication.py`](https://github.com/aboyalejandro/change_data_capture_tutorial/blob/dfbd3f8201989c58e48425d5be4c7afd2a4cf57f/scripts/cdc_logical_replication.py#L59).
- `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` work properly.
- This feature doesn’t replicate sequences, DDLs or schemas.
- Schema changes are ignored. Adding or dropping columns will do nothing. Afterwards the replication will be broken.
- If you have `ALL TABLES` included in your publication and you create a table, you need to also add it on the target database, otherwise it will just ignore it. 
- If you have `ALL TABLES` included in your publication and you drop a table, replication will be broken.

To run the project, you can do: 

```sh
make build
NUM_RECORDS=10000 make run #Default to 5000 if not specified
```

## 🚀 Start CDC:
Docker will start by default with the wal_level set as 'logical'. Open another terminal and run:

```sh 
make cdc-logical-replication
```
This will apply the following things on each side:

- **Source/Publisher**
  - Check if a replication slot exists.
  - Create a replication slot.
  - Create a publication.
- **Target/Subscriber**
  - Create a subscription to the publisher.

## 🔃 Make changes:

These scripts will run `INSERT`, `UPDATE`, `DELETE` to the 3 generated tables on `generate_data.py`.   

```sh 
NUM_RECORDS=500 make insert-data 
NUM_RECORDS=500 make delete-data
NUM_RECORDS=500 make update-data
make truncate
```

Or you can run single commands directly on the source database if you prefer. 

## ✅ Check with queries (Source):
To query databases like to use DBeaver, but you can use VSCode or psql if you prefer. 

Validate the CDC process is OK on the Source/Publisher side. You should see the listed tables you are replicating and the `cdc_tutorial_slot`:

```sql
select * from pg_publication_tables;
select * from pg_replication_slots;
```

## ✅ Check with queries (Target):

Validate the CDC is OK on the Target/Subscriber side. You should see the listed subscription:

```sql
select * from pg_subscription;
```
Count rows after running `INSERT` or `DELETE` in real-time:

```sql
select count(*) from products;
select count(*) from user_profiles;
select count(*) from transactions;
```
Validate after `UPDATE`:

```sql
select max(updated_at) from products;
select max(updated_at) from user_profiles;
select max(updated_at) from transactions;
```

## 🔨 Break the replication: 

Note: The scripts are limited to `TRUNCATE`, `DROP`, `INSERT`, `UPDATE` or `DELETE` `transactions`, `products` and `user_profiles`. `CREATE TABLE` will add a new table randomly. If you ended up dropping all the tables, you can do Ctrl+C and `make restart` to spin-up the project again. 

```sh
make create-table 
make drop-table 
```

If you don't have the publication set for ALL TABLES, you should follow this process after creating a new table:

```sql
ALTER PUBLICATION cdc_tutorial ADD TABLE stores;
ALTER PUBLICATION cdc_tutorial DROP TABLE stores;
```

You should this next to each other since the 'subtype' column will be removed:

```sh
make add-column 
make drop-column 
```

Remember to always check on Target Database if the changes are resulting or not.

### 😎 [Follow me on Linkedin](https://www.linkedin.com/in/alejandro-aboy/)
- Get tips, learnings and tricks for your Data career!

### 📩 [Subscribe to The Pipe & The Line](https://thepipeandtheline.substack.com/?utm_source=github&utm_medium=referral)
- Join the Substack newsletter to get similar content to this one and more to improve your Data career!

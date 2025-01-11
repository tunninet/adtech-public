# AdTech MongoDB Setup and Seeding

This directory shows how to:

1. **Create** a dedicated MongoDB user (`adtech`) and empty DB (`adtech`) via `mongocli` or `mongo` shell.
2. **Build** and **run** a Docker-based seeding script (`seed_ads.py`) that inserts sample ad docs into the `adtech.ads` collection.
3. **Store** credentials in a Kubernetes Secret and run a **Kubernetes Job** to seed the data.

## Prerequisites

- **MongoDB** is running as a **replica set**, with a known **admin** user or root user.  
- **mongocli** (or `mongo` shell) installed locally to create DB + user.
- **Docker** environment to build the seeding image.
- **Kubernetes** cluster & privileges to create secrets and jobs.

---

## Step 1: Create the `adtech` Database and User with `mongocli`

### 1. Connect as Admin - If using the load balancer, keep re-connecting until you have primary replica access

Example:

mongocli shell \
  --host "<YOUR_MONGODB_FQDN>" \
  --port 27017 \
  -u "root" \
  -p "<YOUR_PASSWORD>" \
  --authenticationDatabase "admin"

### 2. Create the DB & User

use adtech      // Switch to or create the 'adtech' database
switched to db adtech

db.createUser({
    user: "adtech",
    pwd: "<YOUR_PASSWORD>",
    roles: [
      // Example: dbOwner covers readWrite/dbAdmin
      { role: "dbOwner", db: "adtech" }
    ]
})

Successfully added user: {
  "user" : "adtech",
  "roles" : [
    {
      "role" : "dbOwner",
      "db" : "adtech"
    }
  ]
}

- Alternatively, if you prefer separate roles:
- roles: [ { role: "readWrite", db: "adtech" }, { role: "dbAdmin", db: "adtech" } ]
- exit (if using true cli vs compass UI)

## Step 2: Seeding the Mongo `ads` Collection

1. **Build and push** the `db-seed` container:

   cd db-seed
   docker build -t <YOUR_REGISTRY_FQDN>:5000/db-seed:latest .
   docker push <YOUR_REGISTRY_FQDN>:5000/db-seed:latest

2. **Create a Kubernetes Secret with Credentials**

kubectl create secret generic adtech-mongo-secret \
  --from-literal=MONGO_USER='adtech' \
  --from-literal=MONGO_PASS='<YOUR_PASSWORD>' \
  --from-literal=MONGO_DB='adtech' \
  --namespace adtech

3. **Apply the Job**

kubectl apply -f job-db-seed.yaml -n adtech

kubectl logs job/seed-ads-job -n adtech --follow

You should see:

    [seed_db] Connecting to MongoDB URI:
    mongodb://adtech:***@<YOUR_MONGODB_FQDN>:27017,...
    [seed_db] Clearing out old docs...
    [seed_db] Inserting docs for user IDs 1..10 plus 'default' doc...
    [seed_db] Done seeding 'ads' collection with user IDs 1..10 plus 'default'.

4. **Verify**

use adtech
db.ads.find().pretty()

You should see _id in ["1","2","3",...,"10","default"]

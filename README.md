# igumaSQL

Welcome to **igumaSQL**, a simple, lightweight, and extensible SQL database system written in Python. **igumaSQL** allows you to create, store, and query data with built-in features like horizontal scaling (sharding) and vertical scaling (partitioning) to help manage larger datasets efficiently.

## Key Features

### 1. **Basic SQL Operations**
   - **SELECT**: Retrieve specific columns from tables with optional conditions.
   - **INSERT**: Add new rows to your tables.

### 2. **Horizontal Scaling (Sharding)**
   - Split large tables into multiple files (shards) based on row count. This allows for the distribution of data across multiple files, enabling better management of large datasets.
   - Automatically divides tables into smaller chunks (shards) to ensure optimal performance when handling high-volume data.
   - Example usage:
     ```sql
     HORIZONTAL SCALING users
     ```

### 3. **Vertical Scaling (Partitioning)**
   - Partition a table by dividing it into multiple smaller tables based on column groups. This allows you to separate data logically and store them in distinct files.
   - You can define specific column groups (partitions) that are stored in separate files for faster querying.
   - Example usage:
     ```sql
     VERTICAL SCALING users name, age
     ```

### 4. **Data Storage**
   - Tables are stored as JSON files on disk for simplicity and portability.
   - Each table is saved with its data and column structure, and can be easily loaded back into memory for querying.

### 5. **Flexible Querying**
   - **SELECT** queries allow you to retrieve specific columns from a table, with support for simple conditions like `WHERE`.
   - **INSERT** queries allow you to add new rows to a table with specified columns and values.

### 6. **Easy Table Management**
   - Create tables by specifying columns and start inserting rows directly.
   - Save and load tables with ease, and scale them as needed based on dataset size and complexity.

## Example Usage

1. **Insert Data**
   To insert data into a table:
   ```sql
   INSERT INTO users (name, age) VALUES ('Alice', 30)
   ```

2. **Select Data To retrieve data from a table:**
    ```sql
    SELECT name, age FROM users WHERE age > 25
    ```
3.**Scale Tables Horizontally (Sharding) To shard a table into multiple files:**

```sql
HORIZONTAL SCALING users
```

4. **Scale Tables Vertically (Partitioning) To partition a table by columns:**
```sql
VERTICAL SCALING users name, age
```

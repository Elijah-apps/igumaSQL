import json
import os
import re

# Table class represents a table in the database
class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns  # List of column names
        self.rows = []          # List of rows (data)
    
    def save(self, shard_num=None):
        # Save the table data to a JSON file
        filename = f"{self.name}_shard{shard_num}.json" if shard_num else f"{self.name}.json"
        with open(filename, "w") as file:
            json.dump({"columns": self.columns, "rows": self.rows}, file)

    @staticmethod
    def load(name, shard_num=None):
        # Load the table from a JSON file
        filename = f"{name}_shard{shard_num}.json" if shard_num else f"{name}.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                data = json.load(file)
                table = Table(name, data["columns"])
                table.rows = data["rows"]
                return table
        return None


# Simple SQL Parser
def parse_query(query):
    # Match SELECT queries: SELECT col1, col2 FROM table WHERE condition
    select_match = re.match(r"SELECT (.+) FROM (\w+)(?: WHERE (.+))?", query)
    if select_match:
        columns = select_match.group(1).split(", ")
        table = select_match.group(2)
        condition = select_match.group(3) if select_match.group(3) else None
        return {"type": "SELECT", "columns": columns, "table": table, "condition": condition}

    # Match INSERT INTO queries: INSERT INTO table (col1, col2) VALUES (val1, val2)
    insert_match = re.match(r"INSERT INTO (\w+) \((.+)\) VALUES \((.+)\)", query)
    if insert_match:
        table = insert_match.group(1)
        columns = insert_match.group(2).split(", ")
        values = insert_match.group(3).split(", ")
        return {"type": "INSERT", "table": table, "columns": columns, "values": values}
    
    return None


# Execute a SELECT query
def execute_select(query, tables):
    parsed_query = parse_query(query)
    if parsed_query and parsed_query["type"] == "SELECT":
        table_name = parsed_query["table"]
        columns = parsed_query["columns"]
        condition = parsed_query["condition"]

        table = tables.get(table_name)
        if table:
            results = []
            for row in table.rows:
                if condition:
                    # For simplicity, just support one condition (e.g., "age > 30")
                    if eval(f"row['{condition.split()[0]}'] {condition.split()[1]} {condition.split()[2]}"):
                        results.append({col: row[col] for col in columns})
                else:
                    results.append({col: row[col] for col in columns})
            return results
    return []


# Execute an INSERT query
def execute_insert(query, tables):
    parsed_query = parse_query(query)
    if parsed_query and parsed_query["type"] == "INSERT":
        table_name = parsed_query["table"]
        columns = parsed_query["columns"]
        values = parsed_query["values"]
        
        table = tables.get(table_name)
        if table:
            new_row = dict(zip(columns, values))
            table.rows.append(new_row)
            table.save()
            return True
    return False


# Horizontal Scaling - Sharding (Distribute across files)
def horizontal_scaling(tables, table_name, shard_size=5):
    # Split rows of a table into multiple shards if rows exceed shard_size
    table = tables.get(table_name)
    if not table:
        return

    rows = table.rows
    num_shards = (len(rows) // shard_size) + (1 if len(rows) % shard_size else 0)

    # Create shards and save them
    for i in range(num_shards):
        shard_rows = rows[i * shard_size:(i + 1) * shard_size]
        shard_table = Table(table_name, table.columns)
        shard_table.rows = shard_rows
        shard_table.save(shard_num=i)
    return True


# Vertical Scaling - Partitioning (Split into different files based on column groups)
def vertical_scaling(tables, table_name, partition_columns):
    # Partition columns into different sets and store each set in a separate file
    table = tables.get(table_name)
    if not table:
        return

    num_partitions = len(partition_columns)
    for i, cols in enumerate(partition_columns):
        partition_table = Table(table_name, cols)
        partition_table.rows = [{col: row[col] for col in cols} for row in table.rows]
        partition_table.save(shard_num=i)
    return True


# Main function to interact with the database
def main():
    # In-memory storage for loaded tables
    tables = {}

    # Load existing tables
    for filename in os.listdir():
        if filename.endswith(".json"):
            table_name = filename.split("_")[0]
            if table_name not in tables:
                tables[table_name] = Table.load(table_name)

    # Sample interaction
    while True:
        query = input("Enter SQL query (or 'exit' to quit): ").strip()
        if query.lower() == "exit":
            break

        if query.startswith("SELECT"):
            results = execute_select(query, tables)
            if results:
                print("Results:")
                for row in results:
                    print(row)
            else:
                print("No results found.")
        
        elif query.startswith("INSERT"):
            success = execute_insert(query, tables)
            if success:
                print("Insert successful.")
            else:
                print("Insert failed.")

        elif query.startswith("HORIZONTAL SCALING"):
            table_name = query.split()[2]
            success = horizontal_scaling(tables, table_name)
            if success:
                print(f"Table {table_name} scaled horizontally.")
            else:
                print(f"Failed to scale {table_name}.")
        
        elif query.startswith("VERTICAL SCALING"):
            table_name, *columns = query.split()[2:]
            columns = [col.split(",") for col in columns]
            success = vertical_scaling(tables, table_name, columns)
            if success:
                print(f"Table {table_name} scaled vertically.")
            else:
                print(f"Failed to scale {table_name}.")
        
        else:
            print("Unsupported query.")


if __name__ == "__main__":
    main()

# Take Off Assignment

This repo contains solutions to the tasks required by Take Off. The assignment includes tasks in Python, Odoo development, SQL, Linux scripting, and Git version control.

## Table of content
- [python generator](#python-generator)
- [Odoo Module : Custom Products and Partners](#odoo-module--custom-products-and-partners)
- [Odoo CLI Script for Sales Orders](#odoo-cli-script-for-sales-orders)
- [SQL Queries for Stock Management](#sql-queries-for-stock-management)
- [Linux Scripting](#linux-scripting)

## Python Generator

### Requirment 
Write a simple generator that will respond with a next number starting from 0 up to 9 and then from beginning. Include 24 iterations into `__main__` to show results.

### implementation 
The script defines a generator function `number_generator()` that yields numbers from `0` to `9` in an infinite loop. In the main block, the generator is iterated **24 times**, printing each number to the console.

### Refrences 
[Python Generators Wiki](https://wiki.python.org/moin/Generators).

## Odoo Module : Custom Products and Partners

### Requirement
**Task 2.1**: Create a simple Odoo module with a `data` directory only, containing a custom consumable product (`product.template` + `product.product`) and partner info (`res.partner`), defined for later access by XML ID.

### Implementation
We developed an Odoo module that defines custom products and partners relevant to a retail and wholesale business like **Take Off**. The module includes product templates with attributes, variants, categories, and partner information, covering multiple business scenarios.

### Module Structure
```plaintext
odoo_module
└── custom_products_partners
    ├── data
    │   ├── attributes.xml  <-- Defines product attributes like size, color, material
    │   ├── partners.xml    <-- Defines partners (brands, agents, distributors, etc.)
    │   └── products.xml    <-- Defines custom products (consumable, variant products)
    ├── __init__.py
    └─── __manifest__.py     <-- Module manifest file
```

### Instructions for Module Installation
1. **Place the Module in Addons Path**
   - Place the `odoo_module` directory in your Odoo `addons` path.

2. **Update the App List**
   - Navigate to **Apps** > **Update Apps List** in the Odoo interface.
   - You might need to confirm the action.

3. **Install the Module**
   - Search for **Custom Products and Partners** in the Apps.
   - Click **Install** to add the module to your Odoo instance.

4. **Enable Product Variants Manually**
   - **Important**: Since the module includes product variants, you need to enable the **Variants** feature manually:
     - Go to **Inventory** > **Configuration** > **Settings**.
     - Under the **Products** section, locate the **Variants** option.
     - Check the box to enable **Variants**.
     - Click **Save** to apply the changes.

### Future Enhancement
An enhancement suggestion is to automate enabling **Product Variants**. This would eliminate the need for manual configuration by setting the required parameters programmatically.


## Odoo CLI Script for Sales Orders

### Requirement
**Task 2.2**: Write a CLI script that will connect to Odoo via RPC with the host, port, user, and password defined in a `.env` file. Using the product and customer created in Task 2.1, create and confirm a Sales Order (SO). Print the SO name, SO lines (product name, price, quantity), and a list of transfers with their states to the console. No need to manage routes and locations; default settings are sufficient.

### Implementation
We developed a Python CLI script named `create_sales_order.py` that performs the following actions:

1. **Connect to Odoo**: Establishes an RPC connection using credentials from a `.env` file.
2. **Create a Sales Order**: Utilizes the custom product and the fixed partner "CLI Client" to create a new Sales Order.
3. **Confirm the Sales Order**: Validates the Sales Order to generate associated stock transfers.
4. **Print Details**: Outputs the Sales Order name, line items (product name, price, quantity), and associated stock transfers with their states to the console.

### Instructions for Script Usage

1. **Ensure `.env` File is Configured**
   
   - Place a `.env` file in the `cli_scripts` directory (`takeoff_assignment/cli_scripts`) with the following content:
   
     ```ini
     ODOO_HOST=localhost
     ODOO_PORT=PORT
     ODOO_DB=your_database_name
     ODOO_USER=your_username
     ODOO_PASSWORD=your_password
     ```
   
   > **Security Note**: Add the `.env` file to your `.gitignore` to prevent sensitive information from being pushed to version control.

2. **Install Required Python Packages**
   
   Ensure you have the necessary Python packages installed. From the project root, activate your virtual environment and install the dependencies:
   
   ```bash
   pip install odoorpc python-dotenv
   ```

3. **Run the CLI Script**
   
   Navigate to the `cli_scripts` directory and execute the script:
   
   ```bash
   cd cli_scripts
   python3 create_sales_order.py
   ```

### Script Usage with Command-Line Arguments

The `create_sales_order.py` script supports the following optional command-line arguments:

- `--product`: Name of the product (default: `Bulk Apparel Pack`)
- `--quantity`: Quantity of the product (default: `5`)
- `--price`: Price per unit of the product (default: product's list price)

**Example Usage:**

```bash
python3 create_sales_order.py --product "Bulk Footwear Pack" --quantity 10 --price 30.0
```

**Note:** All Sales Orders created using this script will automatically be associated with hardcoded "CLI Client" partner.

To fulfill **Task 3.1**, where we need to add stock dynamically based on the Sales Orders created via the CLI script, we utilize the "CLI Client" as a unique identifier for these orders. Here's why and how:
   
   - **Simplified Identification:** By hardcoding the partner to "CLI Client", we ensure that all Sales Orders created by the CLI script are easily identifiable in the database. This eliminates the need for additional fields or complex filtering.
 
   - **Simpler Approach:** While a more accurate method would involve adding a custom field (e.g., `is_cli_order`) to the `sale.order` model to flag CLI-created orders, this would conflict with the project requirement of creating a simple Odoo module with only a `data` directory.
   
   - **Demonstrated Capability:** By using the fixed partner name, we adhere to the module constraints and still achieve the necessary functionality. This approach effectively demonstrates our ability to work with SQL queries and manage data dynamically.

## SQL Queries for Stock Management

### Requirement
**Task 3.1**: Write a simple SQL query (or queries) that will add stock for the product defined in Task 2.1 with the exact quantity required for the Sales Orders (SOs) created in Task 2.2.

**Task 3.2**: Write an SQL query to list all products available in stock (available quantity > 0). Resulting columns should be: article name, default code, warehouse name, location full name, on-hand quantity, and available quantity.

### Implementation

#### 3.1 Add Stock Based on Confirmed SOs

We created an SQL query in `add_stock.sql` that aggregates the total quantity of products ordered by the **CLI Client** (hardcoded in Task 2.2) from confirmed Sales Orders (`sale` state). The query then adds the exact quantity required for each product to the warehouse stock. Here's a breakdown of the steps:

1. **Identify CLI Sales Orders**: 
   - The query identifies Sales Orders where the partner is **CLI Client** and the order is confirmed (`sale` state).

2. **Aggregate Quantities**:
   - The query calculates the total quantity ordered for each product across all confirmed Sales Orders for **CLI Client**.

3. **Retrieve Stock Location**:
   - The warehouse stock location (`WH/Stock`) is retrieved to add stock in the appropriate warehouse.

4. **Insert Stock**:
   - The exact quantity required for each product is inserted into the `stock_quant` table, which manages stock levels in Odoo.

**Why `reserved_quantity = 0`?**  
Given that the products we are handling are **consumables**, they do not require reservations like storable products. Consumables are immediately available for use or sale without any need for reservations. By setting the `reserved_quantity` to zero, we ensure that the entire added stock is available for future orders or operations without manual reservation management.

#### 3.2 List Products with Available Stock

To verify the stock added by Task 3.1, we created a second query, `verify_stock_dynamic.sql`, that lists all products with available stock (i.e., available quantity > 0).
This query helps ensure that the stock adjustment performed in Task 3.1 is reflected accurately in the system.

### Leveraging the Hardcoded "CLI Client" for Simplicity

In Task 2.2, we hardcoded the partner to **CLI Client** to simplify identification of Sales Orders created via the CLI script. This approach ensures that all CLI-created orders are easily identifiable in the database, allowing us to track and manage stock adjustments related to these orders efficiently. 

While a more advanced approach would involve adding a custom field (e.g., `is_cli_order`) to the `sale.order` model to explicitly flag CLI-created orders, this would require inheriting the model, which conflicts with the requirement to create a simple Odoo module with only a `data` directory. By using the fixed partner name, we can still achieve the desired functionality with minimal complexity while demonstrating our ability to work with SQL queries and manage data dynamically.

## Linux Scripting

### Requirement
**Task 4**: Write a simple bash script that will accept 2 parameters - model name and path to a log file. The script should display all warnings, errors, and critical messages from the defined Odoo log file related to the specified model name.

### Implementation
We developed a bash script named `filter_odoo_logs.sh` located in the `bash_scripts` directory. This script filters Odoo log files to extract entries related to a specific model with severity levels of **WARNING**, **ERROR**, and **CRITICAL**. This functionality is essential for monitoring and troubleshooting by allowing focused inspection of relevant log entries.

#### Script Details

- **Filename:** `filter_odoo_logs.sh`
- **Location:** `bash_scripts/filter_odoo_logs.sh`
- **Permissions:**  
  Ensure the script is executable by running:
  ```bash
  chmod +x bash_scripts/filter_odoo_logs.sh
  ```
#### Explanation of the Script

1. **Parameter Validation:**
   - The script expects exactly two arguments: `<model_name>` and `<log_file_path>`.
   - If the arguments are missing or incorrect, it displays usage instructions and exits.

2. **Log File Verification:**
   - Checks whether the specified log file exists.
   - If not, it outputs an error message and exits.

3. **Log Filtering Process:**
   - Uses `grep -E` to search for lines containing any of the defined severity levels: `WARNING`, `ERROR`, or `CRITICAL`.
   - Pipes the result to another `grep` to further filter lines that contain the specified model name.
   - Outputs the final filtered log entries to the console.

#### Usage Example

**Basic Usage (Display on Console):**

   ```bash
   ./bash_scripts/filter_odoo_logs.sh sale.order /var/log/odoo/odoo.log
   ```

   **Sample Output:**
   ```plaintext
   2024-09-21 17:23:39,123  WARNING sale_order.py:456 - Error processing model sale.order
   2024-09-21 17:25:10,456  ERROR sale_order.py:789 - Failed to create sale.order SO/00035
   2024-09-21 17:30:15,789  CRITICAL sale_order.py:890 - Critical failure in sale.order processing
   ```


[def]: #linux-scripting
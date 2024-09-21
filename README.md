# Take Off Assignment

This repo contains solutions to the tasks required by Take Off. The assignment includes tasks in Python, Odoo development, SQL, Linux scripting, and Git version control.

## Table of content
- [python generator](#python-generator)
- [Odoo Module : Custom Products and Partners](#odoo-module--custom-products-and-partners)

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
2. **Create a Sales Order**: Utilizes the custom product and partner to create a new Sales Order.
3. **Confirm the Sales Order**: Validates the Sales Order to generate associated stock transfers.
4. **Print Details**: Outputs the Sales Order name, line items (product name, price, quantity), and associated stock transfers with their states to the console.

### Instructions for Script Usage

1. **Ensure `.env` File is Configured**
   
   - Place a `.env` file at the cli scripts directory (`takeoff_assignment/cli_scripts`) with the following content:
   
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

- `--partner`: Name of the partner/customer (default: 'test client')
- `--product`: Name of the product (default: 'Stylish T-Shirt')
- `--quantity`: Quantity of the product (default: 5)
- `--price`: Price per unit of the product (default: product's list price)

**Example Usage:**

```bash
python3 create_sales_order.py --partner "Adidas AG" --product "Stylish T-Shirt" --quantity 10 --price 30.0
```

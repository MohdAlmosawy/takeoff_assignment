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

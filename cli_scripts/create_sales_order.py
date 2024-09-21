import os
import sys
import odoorpc
import argparse
from dotenv import load_dotenv

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(env_path):
        print("Error: .env file not found. Please create one with the required Odoo connection details.")
        sys.exit(1)
    load_dotenv(env_path)

def connect_odoo():
    host = os.getenv('ODOO_HOST')
    port = int(os.getenv('ODOO_PORT'))
    db = os.getenv('ODOO_DB')
    user = os.getenv('ODOO_USER')
    password = os.getenv('ODOO_PASSWORD')

    try:
        odoo = odoorpc.ODOO(host, port=port)
        odoo.login(db, user, password)
        print(f"Connected to Odoo at {host}:{port}, Database: {db}, User: {user}")
        return odoo
    except Exception as e:
        print(f"Failed to connect to Odoo: {e}")
        sys.exit(1)

def get_model(odoo, model_name):
    try:
        model = odoo.env[model_name]
        return model
    except Exception as e:
        print(f"Failed to access model '{model_name}': {e}")
        sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser(description='Create and confirm a Sales Order in Odoo.')
    parser.add_argument('--product', type=str, help='Name of the product')
    parser.add_argument('--quantity', type=float, help='Quantity of the product')
    parser.add_argument('--price', type=float, help='Price per unit of the product')

    args = parser.parse_args()
    return args

def main():
    # Load environment variables
    load_env()

    # Parse command-line arguments
    args = parse_arguments()

    # Set default values
    DEFAULT_PARTNER_NAME = 'CLI Client'
    DEFAULT_PRODUCT_NAME = 'Bulk Apparel Pack'
    DEFAULT_QUANTITY = 5
    DEFAULT_PRICE_UNIT = None 

    # Set partner name to 'CLI Client' without allowing overrides
    partner_name = DEFAULT_PARTNER_NAME

    # Use command-line arguments if provided, else use defaults
    product_name = args.product if args.product else DEFAULT_PRODUCT_NAME
    quantity = args.quantity if args.quantity else DEFAULT_QUANTITY
    price_unit = args.price if args.price else DEFAULT_PRICE_UNIT

    # Connect to Odoo
    odoo = connect_odoo()

    # Access necessary models
    product_product_model = get_model(odoo, 'product.product')
    partner_model = get_model(odoo, 'res.partner')
    sale_order_model = get_model(odoo, 'sale.order')

    # Retrieve product and partner IDs by name
    try:
        # Search for the partner by name (case-insensitive)
        partner_ids = partner_model.search([('name', '=ilike', partner_name)])
        if not partner_ids:
            print(f"Error: Partner '{partner_name}' not found.")
            sys.exit(1)
        partner_id = partner_ids[0]
        partner_record = partner_model.browse(partner_id)
        print(f"Partner ID: {partner_id}, Name: {partner_record.name}")

        # Search for the product by name (case-insensitive)
        product_ids = product_product_model.search([('name', '=ilike', product_name)])
        if not product_ids:
            print(f"Error: Product '{product_name}' not found.")
            sys.exit(1)
        product_id = product_ids[0]
        product_record = product_product_model.browse(product_id)
        print(f"Product ID: {product_id}, Name: {product_record.name}")

        # Get the default price if price_unit is None
        if price_unit is None:
            price_unit = product_record.list_price
    except Exception as e:
        print(f"Error retrieving records: {e}")
        sys.exit(1)

    # Create a Sales Order
    try:
        sale_order = sale_order_model.create({
            'partner_id': partner_id,
            'order_line': [(0, 0, {
                'product_id': product_id,
                'product_uom_qty': quantity,  # Quantity desired
                'price_unit': price_unit,     # Unit price
            })],
        })
        print(f"Sales Order Created with ID: {sale_order}")
    except Exception as e:
        print(f"Failed to create Sales Order: {e}")
        sys.exit(1)

    # Confirm the Sales Order
    try:
        sale_order_record = sale_order_model.browse(sale_order)
        sale_order_record.action_confirm()
        print(f"Sales Order {sale_order_record.name} confirmed.")
    except Exception as e:
        print(f"Failed to confirm Sales Order {sale_order}: {e}")
        sys.exit(1)

    # Retrieve and print Sales Order details
    try:
        print("\n--- Sales Order Details ---")
        print(f"Sales Order Name: {sale_order_record.name}")
        print("Sales Order Lines:")
        for line in sale_order_record.order_line:
            print(f" - Product: {line.product_id.name}, Price: {line.price_unit}, Quantity: {line.product_uom_qty}")
    except Exception as e:
        print(f"Error retrieving Sales Order details: {e}")
        sys.exit(1)

    # Retrieve and print associated Stock Transfers (Pickings)
    try:
        # Fetch pickings associated with the sales order
        pickings = sale_order_record.picking_ids
        print("\n--- Stock Transfers ---")
        for picking in pickings:
            print(f" - Transfer: {picking.name}, State: {picking.state}")
    except Exception as e:
        print(f"Error retrieving Stock Transfers: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
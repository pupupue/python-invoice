import jinja2
import pdfkit
from datetime import datetime
import pandas as pd
import pprint


# hardcoded_date = datetime.fromisoformat('2023-09-13').strftime("%d %b, %Y")
# hardcoded_due_date = datetime.fromisoformat('2023-09-13').strftime("%d %b, %Y")
# today_date = datetime.today().strftime("%d %b, %Y")
# month = datetime.today().strftime("%B")

def getDate ():
  date = {
    'issued': datetime.fromisoformat('2023-09-13').strftime("%d %b, %Y"),
    'due': datetime.fromisoformat('2023-09-13').strftime("%d %b, %Y"),
  }
  return date

def parse_product_string(product_string):
    # Split the input string into items using comma as delimiter
    items = product_string.split(',')

    products = {}  # Dictionary to store product names as keys and quantities as values

    for item in items:
        # Split each item by "×" to separate quantity and product name
        parts = item.strip().split('×')
        if len(parts) == 2:
            quantity = int(parts[0].strip())  # Convert quantity to integer
            product_name = parts[1].strip()  # Remove leading/trailing spaces from product name
            products[product_name] = quantity

    return products

def getItem (item_name, q):
  products_df = pd.read_csv('./input/products.csv', header=0)
  product_df = products_df[products_df["Product title"] == item_name]
  name = item_name
  quantity = q
  rate = float(product_df['Price'])
  amount = quantity * rate
  return {
    'name': name,
    'quantity': quantity,
    'rate': "%.2f" % rate,
    'amount': "%.2f" % amount
  }

def calculateTotalAmount(items):
    total_amount = 0
    for item in items:
        total_amount += float(item['amount'])
    return total_amount

def getOrderDetails(items):
  subtotal_amount = calculateTotalAmount(items)
  tax_amount = 0
  shipping_amount = 15
  total_amount = subtotal_amount + tax_amount + shipping_amount

  return {
    'subtotal_amount': "%.2f" % subtotal_amount,
    'tax_amount': "%.2f" % tax_amount,
    'shipping_amount': "%.2f" % shipping_amount,
    'total_amount': "%.2f" % total_amount,
  }


def getCustomer(order):
  billing = {
    'name': order['Billing Name'],
    'address': order['Billing Address'],
  }
  shipping = {
    'name': order['Shipping Name'],
    'address': order['Shipping Address'],
  }
  return {
    'billing': billing,
    'shipping': shipping,
  }

company = {
  'legal_entity': 'LAURINS CERAMICS PTE. LTD.',
  'id': '202336832H',
  'email': 'laurinsceramics@gmail.com',
  'phone': '+371 2 580 6617',
  'website': 'https://laurinsceramics.com/'
}

def main():
  # Read the CSV file with the first line as header
  df = pd.read_csv('./input/orders.csv', header=0)
  orders_df = df[df['Status'] == 'completed']

  for index, order in orders_df.iterrows():
    invoice_nr = order['Order #']
    customer = getCustomer(order)

    items_object = parse_product_string(order['Product(s)'])
    items = []
    for product_name, quantity in items_object.items():
      item = getItem(product_name, quantity)
      items.append(item)

    date = getDate()

    order_details = getOrderDetails(items)

    context = {
      'company': company,
      'items': items,
      'customer': customer,
      'date': date,
      'invoice_nr': invoice_nr,
      'order': order_details
    }

    template_loader = jinja2.FileSystemLoader('./src/')
    template_env = jinja2.Environment(loader=template_loader)

    html_template = 'new-invoice.html'
    template = template_env.get_template(html_template)
    output_text = template.render(context)

    config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
    output_pdf = f'./output/invoice-{invoice_nr}.pdf'
    pdfkit.from_string(output_text, output_pdf, configuration=config,  css='./src/new-invoice.css')

  # invoice_nr = '123'
  # customer = getCustomer()
  # item = getItem()
  # items = [item]
  # date = getDate()
  # order = getOrderDetails(items)

  # context = {
  #   'company': company,
  #   'items': items,
  #   'customer': customer,
  #   'date': date,
  #   'invoice_nr': invoice_nr,
  #   'order': order
  # }
  # template_loader = jinja2.FileSystemLoader('./src/')
  # template_env = jinja2.Environment(loader=template_loader)

  # html_template = 'invoice-template.html'
  # template = template_env.get_template(html_template)
  # output_text = template.render(context)

  # config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
  # output_pdf = 'invoice.pdf'
  # pdfkit.from_string(output_text, output_pdf, configuration=config, css='./src/invoice.css', )




# # from excel you need to split string by comma on 'Products'
# # Order id === invoice id
# # Customer === client_name
# # put this in a fn that you call in the loop
# # refactor html and css for invoice

# context = {
#   'currency': '€',
#   'hardcoded_date': hardcoded_date,
#   'hardcoded_due_date': hardcoded_due_date,
#   'shipping_cost': 15,
#   'tax': 0,
#   'subtotal_price': '123123312',
#   'total_price': '123123312', # subtotal_price + shipping_cost

#   'company': company,
#   'client_name': client_name,
#   'today_date': today_date,
#   'total': f'${total:.2f}',
#   'month': month,
#   'items': [
#     { 'name': 'hello',  'quantity': 1, 'rate': 123, 'amount': 246 },
#     { 'name': 'world', 'price': 321 },
#   ]
#   # 'item1': item1, 'subtotal1': f'${subtotal1:.2f}',
#   # 'item2': item2, 'subtotal2': f'${subtotal2:.2f}',
#   # 'item3': item3, 'subtotal3': f'${subtotal3:.2f}'
# }

# template_loader = jinja2.FileSystemLoader('./src/')
# template_env = jinja2.Environment(loader=template_loader)

# html_template = 'invoice-template.html'
# template = template_env.get_template(html_template)
# output_text = template.render(context)

# config = pdfkit.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")
# output_pdf = 'invoice.pdf'
# pdfkit.from_string(output_text, output_pdf, configuration=config, css='./src/invoice.css', )



if __name__ == "__main__":
  main()
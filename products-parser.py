from datetime import datetime
import pandas as pd
import pprint

map_new_to_old = {
  "Title": "Name",
  "Published": "Visibility in catalog",
  "Body (HTML)": "Description",
  "Variant Price": "Regular price",
  "Product Category": "Categories",
  "Tags": "Categories",
}

from_header = [
  "ID",
  "Type",
  "SKU",
  "Name",
  "Published",
  "Is featured?",
  "Visibility in catalog",
  "Short description",
  "Description",
  "Date sale price starts",
  "Date sale price ends",
  "Tax status",
  "Tax class",
  "In stock?",
  "Stock",
  "Low stock amount",
  "Backorders allowed?",
  "Sold individually?",
  "Weight (kg)",
  "Length (cm)",
  "Width (cm)",
  "Height (cm)",
  "Allow customer reviews?",
  "Purchase note",
  "Sale price",
  "Regular price",
  "Categories",
  "Tags",
  "Shipping class",
  "Images",
  "Download limit",
  "Download expiry days",
  "Parent",
  "Grouped products",
  "Upsells",
  "Cross-sells",
  "External URL",
  "Button text",
  "Position"
]

to_header = [
  "Handle",
  "Title",
  "Body (HTML)",
  "Vendor",
  "Product Category",
  "Type",
  "Tags",
  "Published",
  "Option1 Name",
  "Option1 Value",
  "Option2 Name",
  "Option2 Value",
  "Option3 Name",
  "Option3 Value",
  "Variant SKU",
  "Variant Grams",
  "Variant Inventory Tracker",
  "Variant Inventory Qty",
  "Variant Inventory Policy",
  "Variant Fulfillment Service",
  "Variant Price",
  "Variant Compare At Price",
  "Variant Requires Shipping",
  "Variant Taxable",
  "Variant Barcode",
  "Image Src",
  "Image Position",
  "Image Alt Text",
  "Gift Card",
  "SEO Title",
  "SEO Description",
  "Google Shopping / Google Product Category",
  "Google Shopping / Gender",
  "Google Shopping / Age Group",
  "Google Shopping / MPN",
  "Google Shopping / AdWords Grouping",
  "Google Shopping / AdWords Labels",
  "Google Shopping / Condition",
  "Google Shopping / Custom Product",
  "Google Shopping / Custom Label 0",
  "Google Shopping / Custom Label 1",
  "Google Shopping / Custom Label 2",
  "Google Shopping / Custom Label 3",
  "Google Shopping / Custom Label 4",
  "Variant Image",
  "Variant Weight Unit",
  "Variant Tax Code",
  "Cost per item",
  "Price / International",
  "Compare At Price / International",
  "Status"
]

map_new_to_old = {
  "Title": "Name",
  "Published": "Visibility in catalog",
  "Body (HTML)": "Description",
  "Variant Price": "Regular price",
  "Product Category": "Categories",
  "Tags": "Categories",
}


def main():
  # Read the CSV file with the first line as header
  df = pd.read_csv('./products/products-export.csv', header=0)
  new_df = pd.DataFrame(columns=to_header)
  
  for index, row in df.iterrows():
    # Create an empty row with NaN values
    empty_row = pd.DataFrame([[None] * len(to_header)], columns=to_header)

    # Add values to the empty row one at a time
    empty_row.at[0, "Title"] = row["Name"]
    empty_row.at[0, "Published"] = row["Visibility in catalog"]
    empty_row.at[0, "Body (HTML)"] = row["Description"]
    empty_row.at[0, "Variant Price"] = row["Regular price"]
    empty_row.at[0, "Product Category"] = row["Categories"]
    empty_row.at[0, "Tags"] = row["Categories"]
    
    # Concatenate the row with the DataFrame
    new_df = pd.concat([new_df, empty_row], ignore_index=True)

  # Export the DataFrame to a CSV file
  new_df.to_csv("./products/new-products.csv", index=False) 

if __name__ == "__main__":
  main()
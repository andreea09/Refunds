#!/usr/bin/python

import csv
from functools import reduce

import paypalrestsdk

from paypalrestsdk import Sale

'''
Alright, primetime, this will actually give people money, so be sure about the files you give to it.
Your csv should have 3 columns: E-MAIL, AMOUNT, ID
'''

paypalrestsdk.configure({
  'mode': 'live', #sandbox or live
  'client_id': 'YOUR CLIENT ID',
  'client_secret': 'YOUR SECRET CODE' })

# Configure input and output
data_directory = '/path to your directory'
file_name = 'file name here'
refund_list_file_name = data_directory + file_name + '.csv'
refund_log_file_name = data_directory + file_name + 'Refunds.log'
refund_csv_file_name = data_directory + 'Refunds/' + file_name + 'RefundsDone.csv'

# Read the entire input file into memory
with open(refund_list_file_name) as input_file:
    input_file_raw = csv.reader(input_file, delimiter=',')
    for row in input_file_raw:
      refunds = [{"email": line[0], "amount": float(line[1]), "id": line[2]} for line in input_file_raw]


# Immutable sum of the entire refund.
refund_list = list(map(lambda line: line['amount'], refunds))
total_refund = reduce(lambda x, y: x + y, refund_list)

# Output details about the entire refund
print("Total Number of Refunds: " + str(len(refunds)) + '\n')
print("Total Refunds in GBP: $" + str(total_refund) + '\n')

def super_print(log_file, output_string):
  '''Print to log and to the console.'''
  print(output_string)
  log_file.write(output_string)

# Create output file object in writing mode
log_file = open(refund_log_file_name, 'w')
csv_file = (open(refund_csv_file_name,'w'))

# Process each refund, one by one, may take a long time.
for refund in refunds:
  
  # Generate details for refund that's about to occur
  email = "Processing refund for: " + refund['email'] + '\n'
  amount = "For the amount of: $" + str(refund['amount']) + ' GBP\n'
  charge_id = "Using the charge GBP of: " + refund['id'] + '\n'
  output_string = email + amount + charge_id

  # Output pre-request string
  super_print(log_file, output_string)

  person = refund['email']
  refunded_amount = refund['amount']
  id = refund['id']

  # Construct write line for the charge
  delimiter = ";"
  columns = (str(person), str(refunded_amount), str(id))
  line = delimiter.join(columns) + "\n"

  # Write line to file
  csv_file.write(line)

  # Try to refund, if it fails a message will be printed indicating that.
  try:
    # Actual refund

    sale = Sale.find(refund['id'])

    refund = sale.refund({
      "amount": {
        "total": refund['amount'],
        "currency": "GBP"
      }
    })

    if refund.success():
      response = "PROCESSED PROPERLY! \n"
    else:
      print(refund.error)
  except:
    response = "***********FAILED TO PROCESS*********** \n"

    # Output post-request string
    super_print(log_file, output_string)

# Close output file
log_file.close()
csv_file.close()



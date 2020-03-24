# Refunds
Mass refunds scripts for PayPal and Stripe

Firstly, create a csv with the refunds you want to do, having three columns: E-MAIL, AMOUNT and ID. (transaction ID)
Keep in mind that Stripe amounts are in cents, so you have to multiply everything by 100 in your csv. 
Then, simply use the PayPal or Stripe script by changing the API key and the path to where your csv is saved.
Double-check your csv before running!!

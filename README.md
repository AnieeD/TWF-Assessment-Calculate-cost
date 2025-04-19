🚚 Delivery Cost Calculator API
This API calculates the minimum delivery cost to fulfill an order from multiple warehouse centers using specific logistics and pricing rules.

🌐 Deployed URL
Base URL:
https://twf-assessment-calculate-cost.onrender.com

Endpoint:
POST /calculate-cost

📦 Request Format
Send a POST request to the /calculate-cost endpoint with a JSON body that includes the items and quantities you want to order.

🔧 Example Request (JSON)
pgsql

POST https://twf-assessment-calculate-cost.onrender.com/calculate-cost
Content-Type: application/json
Body:

json

{
  "A": 1,
  "D": 2,
  "H": 3
}
📬 Response Format
The API responds with the minimum delivery cost required to fulfill the given order.

✅ Example Response
json

{
  "minimum_cost": 178.0
}
🚀 How to Use with Postman
Open Postman

Create a new POST request

URL: https://twf-assessment-calculate-cost.onrender.com/calculate-cost

Go to the Body tab

Choose raw

Select JSON from the dropdown

Paste your order like this:

json

{
  "B": 2,
  "E": 1,
  "I": 1
}
Send the request

View the result – You’ll receive the minimum cost in the response.

📁 requirements.txt
Make sure to have this for local setup or deployment:

nginx

flask
gunicorn

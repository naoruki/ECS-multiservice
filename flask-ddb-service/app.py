import os
import logging
import boto3
from flask import Flask, request, render_template_string

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

AWS_REGION = os.environ["AWS_REGION"]
TABLE_NAME = os.environ["TABLE_NAME"]
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(TABLE_NAME)

# Simple HTML form for key-value
DYNAMODB_FORM = """
<!DOCTYPE html>
<html>
  <body>
    <h1>Write Key/Value to DynamoDB</h1>
    <form method="POST" action="/write">
      <label>Key:</label>
      <input type="text" name="key" required/>
      <br/><br/>
      <label>Value:</label>
      <input type="text" name="value" required/>
      <br/><br/>
      <button type="submit">Write to DynamoDB</button>
    </form>
  </body>
</html>
"""

@app.route("/write", methods=["GET", "POST"])
def write():
    if request.method == "GET":
        return render_template_string(DYNAMODB_FORM)

    key = request.form.get("key")
    value = request.form.get("value")

    if not key or not value:
        logger.warning("Key or Value is missing from form data.")
        return "Key or Value is missing.", 400

    try:
        table.put_item(Item={"pk": key, "info": value})
        logger.info("Wrote item (Key: %s, Value: %s) to table '%s'.", key, value, TABLE_NAME)
        return f"Data written to DynamoDB! (Key: {key}, Value: {value})"
    except Exception as exc:
        logger.exception("Error writing to DynamoDB.")
        return f"Error writing to DynamoDB: {str(exc)}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

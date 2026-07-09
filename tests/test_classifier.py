from pprint import pprint

from src.classification.classifier import ComplaintClassifier

classifier = ComplaintClassifier()

result = classifier.classify(
    complaint_text="My product arrived damaged and I want a replacement.",
    order_context={
        "product_name": "Samsung Earbuds",
        "order_value": 2999,
        "delivery_status": "Delivered",
    },
)

print(result)
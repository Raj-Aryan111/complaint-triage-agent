from pprint import pprint

from src.generation.generator import ResponseGenerator

generator = ResponseGenerator()

result = generator.generate(
    complaint_text="My product arrived damaged and I want a replacement.",

    order_context={
        "product_name": "Levis Denim Jacket",
        "product_category": "Fashion",
        "order_value": 5182,
        "delivery_status": "Delivered",
        "customer_tier": "Normal",
    },

    policies=[
        """
Damaged Product:
Approve replacement if stock exists.
Section 4.1 applies.
        """,

        """
Replacement should be shipped within
2 business days.
        """,
    ],

    precedents=[
        """
Complaint:
Customer received damaged jacket.

Resolution:
Replacement approved.

Compensation:
₹200 Coupon
        """,

        """
Complaint:
Customer received damaged shoes.

Resolution:
Replacement approved.
        """,
    ],
)

print("\nGenerated Decision\n")

pprint(result.model_dump())
# Falabella Technical Test

This repository contains the technical test for Falabella.

**Author:** Raul (Software Engineer)

## Screenshotss

1. ![Swagger on django](image.png)
2. ![Search Client](image-1.png)s
3. ![MER](falabella_MER.png)

## Useful Commands

```bash
# Create and activate virtual environment
python3 -m virtualenv env-falabella
source env-falabella/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations client product sale

# Migrate apps
python manage.py migrate

# use the factory to populate the db
python manage.py seed_data

# Run Django development server
python manage.py runserver

# Run tests
python manage.py test
```

## Example JSON

```json
[
  {
    "id": 215,
    "client": {
      "id": 27,
      "first_name": "Eugene",
      "last_name": "Garcia",
      "document": "NIT",
      "document_number": "ci-74011026",
      "email": "janetclarke@example.net",
      "phone": "542-843-7737"
    },
    "sales": [
      {
        "id": 149,
        "product": {
          "id": 30,
          "name": "Wide",
          "sku": "wide6024",
          "description": "Stand place society ok responsibility movement there.",
          "price": "444232.85",
          "stock": 53,
          "category": 15
        },
        "product_price": "444232.85",
        "product_quantity": 2,
        "sale_total": "888465.70",
        "sale_date": "2025-08-09"
      },
      {
        "id": 166,
        "product": {
          "id": 31,
          "name": "Like",
          "sku": "like8107",
          "description": "Over control despite.",
          "price": "444896.99",
          "stock": 65,
          "category": 15
        },
        "product_price": "444896.99",
        "product_quantity": 2,
        "sale_total": "889793.98",
        "sale_date": "2025-08-09"
      },
      {
        "id": 235,
        "product": {
          "id": 29,
          "name": "Entire",
          "sku": "entire1096",
          "description": "First medical smile consider pick community.",
          "price": "614880.69",
          "stock": 79,
          "category": 17
        },
        "product_price": "614880.69",
        "product_quantity": 4,
        "sale_total": "2459522.76",
        "sale_date": "2025-08-09"
      }
    ],
    "billing_total": "4237782.44",
    "billing_date": "2025-08-09"
  },
]
```
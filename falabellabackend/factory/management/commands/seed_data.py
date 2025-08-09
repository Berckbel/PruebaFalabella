from django.core.management.base import BaseCommand
from faker import Faker
import random
from client.models import Client, DocumentType
from product.models import Product, Category
from sale.models import Sale, Billing
fake = Faker()

class Command(BaseCommand):
    help = "Generate dummy data for Client, Product, Sale, and Billing"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING('Deleting existing data...'))
        Billing.objects.all().delete()
        Sale.objects.all().delete()
        Client.objects.all().delete()
        Product.objects.all().delete()
        DocumentType.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Generating dummy data...'))

        # Create document types
        document_types = []
        posible_types = [{'name': 'Cedula'}, {'name': 'Pasaporte'}, {'name': 'NIT'}]
        for type in posible_types:
            doc_type = DocumentType.objects.create(name=type['name'])
            document_types.append(doc_type)
            self.stdout.write(f"DocumentType created: {doc_type.name}")

        # Create clients
        clients = []
        for _ in range(3):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            phone = fake.phone_number()
            document_number = fake.unique.bothify(text='??-########')
            document_type = random.choice(document_types)
            client = Client.objects.create(first_name=first_name, last_name=last_name, email=email, phone=phone, document_number=document_number, document_type=document_type)
            clients.append(client)
            self.stdout.write(f"Client created: {first_name} {last_name} - {email}")

        # Create categories
        categories = []
        for _ in range(3):
            name = fake.word().capitalize()
            category = Category.objects.create(name=name)
            categories.append(category)
            self.stdout.write(f"Category created: {name}")

        # Create products
        products = []
        for _ in range(5):
            name = fake.word().capitalize()
            sku = name.lower() + str(random.randint(1000, 9999))
            description = fake.sentence()
            price = round(random.uniform(100000, 1000000), 2)
            stock = random.randint(50, 100)
            category = random.choice(categories)
            product = Product.objects.create(name=name, sku=sku, description=description, price=price, stock=stock, category=category)
            products.append(product)
            self.stdout.write(f"Product created: {name} - {sku} - ${price}")

        # Create sales
        sales = []
        for _ in range(100):
            product = random.choice(products)
            quantity = random.randint(1, 5)
            product_price = product.price
            total = round(product_price * quantity, 2)
            sale = Sale.objects.create(
                product=product,
                product_price=product_price,
                product_quantity=quantity,
                sale_total=total
            )
            sales.append(sale)
            self.stdout.write(f"Sale created: {product.name} x{quantity} - ${total}")

        # Create billings
        for _ in range(200):
            client = random.choice(clients)
            num_sales = random.randint(1, 4)
            selected_sales = random.sample(sales, num_sales)
            total_billing = sum(s.sale_total for s in selected_sales)

            billing = Billing.objects.create(
                client=client,
                billing_total=total_billing
            )
            billing.sales.set(selected_sales)
            self.stdout.write(f"Billing created for {client.first_name} {client.last_name} - ${total_billing}")

        self.stdout.write(self.style.SUCCESS('Dummy data generated successfully.'))

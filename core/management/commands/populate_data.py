from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, SubCategory, Product, ProductImage
from core.models import Banner, FAQ

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create categories
        categories_data = [
            {'name': 'Ethnic', 'slug': 'ethnic', 'description': 'Traditional ethnic wear'},
            {'name': 'Western', 'slug': 'western', 'description': 'Modern western clothing'},
            {'name': 'Men\'s Wear', 'slug': 'mens-wear', 'description': 'Men\'s clothing collection'},
            {'name': 'Jewellery', 'slug': 'jewellery', 'description': 'Fashion accessories and jewellery'},
            {'name': 'Handbags', 'slug': 'handbags', 'description': 'Designer handbags and purses'},
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Create subcategories
        subcategories_data = [
            {'category': 'Ethnic', 'name': 'Saree', 'slug': 'saree'},
            {'category': 'Ethnic', 'name': 'Lehenga', 'slug': 'lehenga'},
            {'category': 'Ethnic', 'name': 'Kurta', 'slug': 'kurta'},
            {'category': 'Western', 'name': 'Dress', 'slug': 'dress'},
            {'category': 'Western', 'name': 'Gown', 'slug': 'gown'},
            {'category': 'Men\'s Wear', 'name': 'Sherwani', 'slug': 'sherwani'},
            {'category': 'Men\'s Wear', 'name': 'Suit', 'slug': 'suit'},
        ]
        
        for sub_data in subcategories_data:
            category = Category.objects.get(name=sub_data['category'])
            subcategory, created = SubCategory.objects.get_or_create(
                category=category,
                name=sub_data['name'],
                defaults={'slug': sub_data['slug']}
            )
            if created:
                self.stdout.write(f'Created subcategory: {subcategory.name}')
        
        # Create a test user
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'email': 'test@saarvin.com',
                'first_name': 'Test',
                'last_name': 'User',
                'phone': '9876543210'
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write('Created test user: testuser')
        
        # Create sample products
        products_data = [
            {
                'name': 'Elegant Red Lehenga',
                'description': 'Beautiful red lehenga perfect for weddings and special occasions',
                'category': 'Ethnic',
                'subcategory': 'Lehenga',
                'size': 'M',
                'color': 'Red',
                'brand': 'Designer Collection',
                'rental_price_per_day': 1500.00,
                'security_deposit': 5000.00,
                'is_featured': True
            },
            {
                'name': 'Classic Black Suit',
                'description': 'Professional black suit for formal events',
                'category': 'Men\'s Wear',
                'subcategory': 'Suit',
                'size': 'L',
                'color': 'Black',
                'brand': 'Formal Wear Co',
                'rental_price_per_day': 800.00,
                'security_deposit': 3000.00,
                'is_featured': True
            },
            {
                'name': 'Floral Summer Dress',
                'description': 'Light and breezy summer dress with floral print',
                'category': 'Western',
                'subcategory': 'Dress',
                'size': 'S',
                'color': 'Multi',
                'brand': 'Summer Collection',
                'rental_price_per_day': 600.00,
                'security_deposit': 2000.00,
                'is_featured': True
            },
        ]
        
        for prod_data in products_data:
            category = Category.objects.get(name=prod_data['category'])
            subcategory = SubCategory.objects.get(
                category=category,
                name=prod_data['subcategory']
            )
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'description': prod_data['description'],
                    'category': category,
                    'subcategory': subcategory,
                    'owner': test_user,
                    'size': prod_data['size'],
                    'color': prod_data['color'],
                    'brand': prod_data['brand'],
                    'rental_price_per_day': prod_data['rental_price_per_day'],
                    'security_deposit': prod_data['security_deposit'],
                    'is_featured': prod_data['is_featured']
                }
            )
            if created:
                self.stdout.write(f'Created product: {product.name}')
        
        # Create banners
        banners_data = [
            {
                'title': 'Ethnic Fits',
                'subtitle': 'Upto 60% Off',
                'is_active': True,
                'order': 1
            },
            {
                'title': 'Ethnic Vibes',
                'subtitle': 'From ₹999',
                'is_active': True,
                'order': 2
            },
            {
                'title': 'Western Look',
                'subtitle': 'New Launches',
                'is_active': True,
                'order': 3
            },
        ]
        
        for banner_data in banners_data:
            banner, created = Banner.objects.get_or_create(
                title=banner_data['title'],
                defaults=banner_data
            )
            if created:
                self.stdout.write(f'Created banner: {banner.title}')
        
        # Create FAQs
        faqs_data = [
            {
                'question': 'How does the rental process work?',
                'answer': 'Simply browse our collection, select your items, choose rental dates, and we\'ll deliver to your doorstep.',
                'category': 'General',
                'order': 1
            },
            {
                'question': 'What if the item gets damaged?',
                'answer': 'Minor wear and tear is expected, but significant damage will be charged from your security deposit.',
                'category': 'Rental',
                'order': 2
            },
            {
                'question': 'How do I return the items?',
                'answer': 'We provide a return bag with your order. Simply pack the items and schedule a pickup.',
                'category': 'Return',
                'order': 3
            },
        ]
        
        for faq_data in faqs_data:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                defaults=faq_data
            )
            if created:
                self.stdout.write(f'Created FAQ: {faq.question}')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )

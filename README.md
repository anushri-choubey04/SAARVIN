# SAARVIN RENT - Clothing Rental Platform

A comprehensive Django-based clothing rental platform that allows users to rent and lend designer clothing items.

## Features

### User Management
- User registration and authentication
- User profiles with personal information
- Profile picture upload
- User verification system

### Product Management
- Product categories (Ethnic, Western, Men's Wear, etc.)
- Sub-categories (Saree, Lehenga, Kurta, etc.)
- Product listings with images
- Product search and filtering
- Price-based filtering
- Product reviews and ratings

### Rental System
- Shopping cart functionality
- Rental booking system
- Payment processing
- Delivery tracking
- Return management

### Additional Features
- Wishlist functionality
- User stories/feed
- Newsletter subscription
- FAQ system
- Contact form
- Admin dashboard

## Technology Stack

- **Backend**: Django 4.1.5
- **Database**: SQLite (development)
- **Frontend**: HTML, CSS, JavaScript, Tailwind CSS
- **API**: Django REST Framework
- **Image Processing**: Pillow
- **Authentication**: Django's built-in auth system

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd saarvin_rent
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser
```bash
python manage.py createsuperuser
```

### 6. Populate Sample Data
```bash
python manage.py populate_data
```

### 7. Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Default Credentials

- **Admin**: username: `admin`, password: `admin123`
- **Test User**: username: `testuser`, password: `testpass123`

## Project Structure

```
saarvin_rent/
├── accounts/                 # User management app
├── products/                 # Product management app
├── rentals/                  # Rental system app
├── core/                     # Core functionality app
├── templates/                # HTML templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User uploaded files
├── saarvin_rent/            # Project settings
└── manage.py
```

## API Endpoints

### Authentication
- `POST /accounts/api/login/` - User login
- `POST /accounts/api/register/` - User registration
- `POST /accounts/api/logout/` - User logout

### Products
- `GET /shop/` - Product listing
- `GET /product/<id>/` - Product detail
- `GET /api/search/suggestions/` - Search suggestions

### Wishlist
- `POST /api/wishlist/add/` - Add to wishlist
- `POST /api/wishlist/remove/` - Remove from wishlist

### Cart
- `POST /api/cart/add/` - Add to cart

### Newsletter
- `POST /api/newsletter/subscribe/` - Newsletter subscription

## Admin Panel

Access the admin panel at `http://127.0.0.1:8000/admin/` with superuser credentials.

## Frontend Integration

The project includes a fully integrated frontend with:
- Responsive design
- Modern UI with Tailwind CSS
- Interactive JavaScript components
- Image carousels and sliders
- Mobile-friendly navigation

## Key Models

### User
- Extended Django User model with additional fields
- Phone, address, profile picture
- User verification status

### Product
- Product information and pricing
- Category and subcategory relationships
- Multiple product images
- Availability and featured status

### Rental
- Rental transactions
- Start and end dates
- Pricing calculations
- Status tracking

### Cart
- Shopping cart functionality
- Rental date selection
- Quantity management

## Development

### Adding New Features
1. Create models in appropriate app
2. Create migrations: `python manage.py makemigrations`
3. Apply migrations: `python manage.py migrate`
4. Create views and URLs
5. Update templates if needed

### Static Files
- CSS files: `static/css/`
- JavaScript files: `static/js/`
- Images: `static/images/`
- User uploads: `media/`

## Deployment

For production deployment:
1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure media file serving
5. Set up email backend
6. Use environment variables for sensitive data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, email support@saarvin.com or create an issue in the repository.

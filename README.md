# Flask Plant Shop

An E-commerce site built with Flask and Spectre.css.

## Description

An E-commerce site built with Flask a Python web framework that has an admin panel using Flask Admin. It uses sessions for cart management. Only superusers can access the Admin panel. For styling Spectre.css is used.

## Installation

1. Download the Github repo.
```bash
git clone https://github.com/anirbanbiswas04/Flask-Plant-Shop.git
```

2. Installing & activating Virtual Environment 
```bash
pip install virtualenv
```
```bash
py -m venv env
```
```bash
.\env\Scripts\Activate.ps1
```

3. Installing all the required packages 
```bash
pip install -r requirements.txt
```

4. Run the flask project 
```bash
flask run
```

## Usage
1. Create a superuser using `flask createsuperuser name password`.
2. Add products from the admin panel.
3. Visitors can browse products, search them.
4. They can add products to cart and checkout.
5. Admin user or superuser can manage all the orders.

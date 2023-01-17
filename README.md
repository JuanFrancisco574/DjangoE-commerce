# DjangoE-commerce
The repository's objective is to show a personal project of e-commerce built utilizing Django as backend technology and Bootstrap5 as frontend technology. It's important to mention that the frontend design is not responsive.

## Preview of the project
The home page is composed of the most relevant categories of the store and general products. Here are some pictures of the home page.
![index_P1.png](static/images/index_P1.png)
![index_P2.png](static/images/index_P2.png)

The shopping cart works utilizing session in Django so it's possible to add products to the cart even if the user is not logged in. Once the user is logged in the shopping cart of the user is saved in the database.
![ShoppingCart.png](static/images/ShoppingCart.png)

When a particular category is selected the app is going to show the products of that category.
![Category.png](static/images/Category.png)

The checkout page can only be seen by authenticated users, for now, the app is not integrated with any payment tool.
![Checkout.png](static/images/Checkout.png)

## Database design
![DiagramaER_E-comerce.png](static/images/DiagramaER_E-comerce.png)


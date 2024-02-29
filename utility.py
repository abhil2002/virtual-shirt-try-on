# utility.py

def get_product_data(product_id):
    # Replace this with your actual data retrieval logic
    products = [
        {
            'id': 1,
            'name': 'Men\'s Fashion T-Shirt',
            'category': 'T-Shirt',
            'price': 139,
            'image': 'static/shirt_images/shirt_b1.png',
            'description': 'If you want to stay on top of the fashion trends...',
            'small_images': [
                'static/shirt_images/shirt_b1.png',
                'static/shirt_images/shirt_b2.png',
                'static/shirt_images/shirt_b3.png',
                'static/shirt_images/shirt_b4.png'
                # Add more small images as needed
            ],
        },
        {
            'id': 2,
            'name': 'Another Product',
            'category': 'Some Category',
            'price': 99,
            'image': 'static/shirt_images/shirt_b8.png',
            'description': 'Description for another product...',
            'small_images': [
                'static/shirt_images/shirt_b8.png',
                'static/shirt_images/shirt_b9.png',
                'static/shirt_images/shirt_b10.png',
                'static/shirt_images/shirt_b8.png'
                # Add more small images as needed
            ],
        },
        # Add more products as needed
    ]

    # Find the product with the given ID
    product = next((p for p in products if p['id'] == product_id), None)

    return product

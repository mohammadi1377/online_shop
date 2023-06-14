# from product.models import Product
#
#
# CART_SESSION_ID = 'cart'
#
#
# class Cart:
# 	def __init__(self, request):
# 		self.session = request.session
# 		cart = self.session.get(CART_SESSION_ID)
# 		if not cart:
# 			cart = self.session[CART_SESSION_ID] = {}
# 		self.cart = cart
#
# 	def __iter__(self):
# 		product_ids = self.cart.keys()
# 		products = Product.objects.filter(id__in=product_ids)
# 		cart = self.cart.copy()
# 		for product in products:
# 			cart[str(product.id)]['product'] = product
#
# 		for item in cart.values():
# 			item['total_price'] = int(item['price']) * item['quantity']
# 			item['discount'] = int(item['product'].total_discount) * item['quantity']
# 			item['price_discount'] = item['total_price'] - item['discount']
#
# 			yield item
#
# 	def __len__(self):
# 		return sum(item['quantity'] for item in self.cart.values())
#
# 	def add(self, product, quantity):
# 		product_id = str(product.id)
# 		if product_id not in self.cart:
# 			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
# 		self.cart[product_id]['quantity'] += quantity
# 		self.save()
#
# 	def remove(self, product):
# 		product_id = str(product.id)
# 		if product_id in self.cart:
# 			del self.cart[product_id]
# 			self.save()
#
# 	def save(self):
# 		self.session.modified = True
#
# 	def get_total_price(self):
# 		return sum(int(item['price']) * item['quantity'] for item in self.cart.values())
#
# 	def get_total_discount(self):
# 		return sum(int(item['product'].total_discount) * item['quantity'] for item in self.cart.values())
#
# 	def get_total_price_discount(self):
# 		return self.get_total_price()-self.get_total_discount()
#
# 	def clear(self):
# 		del self.session[CART_SESSION_ID]
# 		self.save()
#
# 	def get_product_quantity(self, product):
# 		product_id = str(product.id)
# 		if product_id in self.cart:
# 			return self.cart[product_id]['quantity']
# 		return 0



from cart.serializers import ProductSerializer
from product.models import Product


CART_SESSION_ID = 'cart'


class Cart:
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(CART_SESSION_ID)
		if not cart:
			cart = self.session[CART_SESSION_ID] = {}
		self.cart = cart

	def __iter__(self):
		product_ids = self.cart.keys()
		products = Product.objects.filter(id__in=product_ids)
		cart = self.cart.copy()

		for product in products:
			serializer = ProductSerializer(product)
			product_data = serializer.data
			product_data['total_discount'] = product.total_discount  # Add the 'total_discount' key
			cart[str(product.id)]['product'] = product_data
			cart[str(product.id)]['product']['pk'] = str(product.id)  # Add the 'pk' attribute

		for item in cart.values():
			item['total_price'] = int(item['price']) * item['quantity']
			item['discount'] = int(item['product']['total_discount']) * item['quantity']
			item['price_discount'] = item['total_price'] - item['discount']

			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def add(self, product, quantity):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
		self.cart[product_id]['quantity'] += quantity
		self.save()

	def remove(self, product):
		product_id = str(product.id)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def save(self):
		self.session.modified = True

	def get_total_price(self):
		return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

	def get_total_discount(self):
		total_discount = 0
		for item in self.cart.values():
			product = item.get('product')
			if product and 'total_discount' in product:
				total_discount += int(product['total_discount']) * item['quantity']
		return total_discount

	def get_total_price_discount(self):
		return self.get_total_price()-self.get_total_discount()

	def clear(self):
		del self.session[CART_SESSION_ID]
		self.save()
# from rest_framework import serializers
# from product.models import Product
#
#
# class CartSerializer(serializers.Serializer):
#     total_price = serializers.SerializerMethodField()
#     total_discount = serializers.SerializerMethodField()
#     total_price_discount = serializers.SerializerMethodField()
#     items = serializers.SerializerMethodField()
#
#     def get_total_price(self, cart):
#         return cart.get_total_price()
#
#     def get_total_discount(self, cart):
#         return cart.get_total_discount()
#
#     def get_total_price_discount(self, cart):
#         return cart.get_total_price_discount()
#
#     def get_items(self, cart):
#         items = cart.__iter__()
#         serialized_items = ItemSerializer(items, many=True).data
#         return serialized_items
#
#
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'total_discount']
#
#
# class ItemSerializer(serializers.Serializer):
#     product = ProductSerializer()
#     total_price = serializers.IntegerField()
#     discount = serializers.IntegerField()
#     price_discount = serializers.IntegerField()
#     quantity = serializers.IntegerField()
#
#
from rest_framework import serializers
from product.models import Product


class CartSerializer(serializers.Serializer):
	total_price = serializers.SerializerMethodField()
	total_discount = serializers.SerializerMethodField()
	total_price_discount = serializers.SerializerMethodField()
	items = serializers.SerializerMethodField()

	def get_total_price(self, obj):
		return obj.get_total_price()

	def get_total_discount(self, obj):
		return obj.get_total_discount()

	def get_total_price_discount(self, obj):
		return obj.get_total_price_discount()

	def get_items(self, obj):
		return list(obj)

	def update_totals(self, obj):
		# Calculate and update the totals manually
		total_price = 0
		total_discount = 0
		for item in obj:
			total_price += item['total_price']
			total_discount += item['discount']
		obj.total_price = total_price
		obj.total_discount = total_discount
		obj.total_price_discount = total_price - total_discount

	def to_representation(self, instance):
		# Update the totals before serializing the instance
		self.update_totals(instance)
		return super().to_representation(instance)


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = ['name', 'price', 'total_discount', 'discount_price']

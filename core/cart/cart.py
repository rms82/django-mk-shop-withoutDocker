from shop.models import Product, ProductStatus

from cart.models import Cart as CartModel
from cart.models import CartItem


class Cart:
    cart_total_price = 0

    def __init__(self, request):
        self.session = request.session

        self.cart = self.session.setdefault(
            "cart",
            {
                "items": [],
            },
        )

    def save(self):
        self.session.modified = True

    def clear(self):
        self.cart = self.session["cart"] = {
            "items": [],
        }
        self.save()

    def is_empty(self):
        return len(self) == 0

    def add_product(self, product_id, quantity=1):
        for item in self.cart["items"]:
            if item["product_id"] == product_id:
                item["quantity"] += 1

                break
        else:
            new_item = {
                "product_id": product_id,
                "quantity": quantity,
            }

            self.cart["items"].append(new_item)

        self.save()

    def update_product_quantity(self, product_id, quantity):
        for item in self.cart["items"]:
            if item["product_id"] == product_id:
                item["quantity"] = quantity

                break
        else:
            return

        self.save()

    def delete_product_item(self, product_id):
        for item in self.cart["items"]:
            if item["product_id"] == product_id:

                self.cart["items"].remove(item)
                self.save()

                break
        else:
            return None

    def get_items(self):
        items = self.cart["items"].copy()
        self.cart_total_price = 0

        for item in items:
            product = Product.objects.get(
                id=item["product_id"], status=ProductStatus.published.value
            )
            product_total_price = int(product.get_price() * item["quantity"])

            item.update(
                {
                    "product_obj": product,
                    "total_price": product_total_price,
                }
            )

            self.cart_total_price += product_total_price

            yield item

    def __len__(self):
        return len(self.cart["items"])

    def cart_total_items(self):
        return sum(item["quantity"] for item in self.cart["items"])

    def cart_from_db(self, user):
        cart_obj, created = CartModel.objects.get_or_create(user=user)
        cart_items = cart_obj.cart_items.all()

        for cart_item in cart_items:
            for item in self.cart["items"]:

                if item["product_id"] == str(cart_item.product.id):

                    cart_item.quantity = item["quantity"]
                    cart_item.save()
                    break
            else:
                new_item = {
                    "product_id": str(cart_item.product.id),
                    "quantity": cart_item.quantity,
                }

                self.cart["items"].append(new_item)
                
        self.cart_to_db(user)
        self.save()

    def cart_to_db(self, user):
        cart_obj, created = CartModel.objects.get_or_create(user=user)

        for item in self.cart["items"]:
            product = Product.objects.get(
                id=item["product_id"], status=ProductStatus.published.value
            )
            cart_item, created = CartItem.objects.get_or_create(cart=cart_obj,product=product)
            cart_item.quantity = item['quantity']
            cart_item.save()
        
        product_ids = [item['product_id'] for item in self.cart["items"]]
        CartItem.objects.filter(cart=cart_obj).exclude(product__id__in=product_ids).delete()
            
        
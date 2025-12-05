from decimal import Decimal
from itertools import product
from uuid import UUID

from src.domain.entities.product import Product
from src.domain.unit_of_work import IUnitOfWork


class ProductService:
    def __init__(self, uow: IUnitOfWork):
        self._uow = uow

    async def  create_product(self, name:str, price: Decimal, stock: int) -> Product:
        async with self._uow as uow:
            product = Product(name=name, price=price, stock=stock)
            saved = await uow.products.save(product)
            await uow.commit()
            return saved

    async def purchase_product(self, product_id: UUID, quantity: int) -> Product:
        async with self._uow as uow:
            product = await uow.products.get_by_id(product_id)
            if not product:
                raise ValueError("Product not found")

            product.reduce_stock(quantity)
            await uow.products.save(product)
            await uow.commit()
            return product
        
    async def get_all_products(self):
        async with self._uow as uow:
            products = await uow.products.list_all()
            if not products:
                raise ValueError("No products")

            return products
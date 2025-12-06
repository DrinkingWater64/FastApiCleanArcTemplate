from decimal import Decimal
from fastapi import HTTPException
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from src.presentation.dependencies import ProductServiceDep

router = APIRouter(prefix="/users")

class ProductCreate(BaseModel):
    name: str
    price: Decimal
    stock: int

class PurchaseRequest(BaseModel):
    quantity: int

@router.post("/")
async def create_product(
        data: ProductCreate,
        service: ProductServiceDep
):
    try:
        product = await service.create_product(data.name, data.price, data.stock)
        return product
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.post("/{product_id}/purchase")
async def purchase_product(
        product_id: UUID,
        data: PurchaseRequest,
        service: ProductServiceDep
):
    try:
        product = await service.purchase_product(product_id, data.quantity)
        return product
    except ValueError as e:
        raise HTTPException(400, str(e))

@router.get("/")
async def get_all_products(
        service: ProductServiceDep
):
    try:
        products = await service.get_all_products()
        return products
    except ValueError as e:
        raise HTTPException(400, str(e))

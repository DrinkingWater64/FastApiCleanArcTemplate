import pytest
from unittest.mock import AsyncMock
from decimal import Decimal
from uuid import uuid4

from src.application.services.product import ProductService
from src.domain.entities.product import Product


# Use pytest.mark.asyncio because the service methods are async
@pytest.mark.asyncio
async def test_create_product_success():
    # 1. Setup Mocks
    mock_uow = AsyncMock()
    # The object returned by `async with`:
    mock_uow_ctx = mock_uow.__aenter__.return_value

    # Make save() return the product
    mock_uow_ctx.products.save.side_effect = lambda p: p

    # 2. Initialize Service
    service = ProductService(mock_uow)

    # 3. Action
    name = "TestGadget"
    price = Decimal("99.99")
    stock = 10

    created_product = await service.create_product(name=name, price=price, stock=stock)

    # 4. Assertions
    assert created_product.name == name
    assert created_product.price == price
    assert created_product.stock == stock

    mock_uow_ctx.products.save.assert_called_once()
    mock_uow_ctx.commit.assert_called_once()


@pytest.mark.asyncio
async def test_purchase_product_success():
    """
    Tests the purchase_product use case orchestration.
    Verifies stock is reduced via domain method, the new state is saved, and committed.
    """
    # 1. Setup Mocks
    mock_uow = AsyncMock()
    mock_uow_ctx = mock_uow.__aenter__.return_value

    product_id = uuid4()

    # Create an existing product entity with stock
    initial_stock = 5
    purchase_quantity = 3
    existing_product = Product(
        id=product_id,
        name="Book",
        price=Decimal("20.00"),
        stock=initial_stock
    )

    # Configure the UoW to return the existing product on lookup
    mock_uow_ctx.products.get_by_id.return_value = existing_product

    # 2. Initialize Service with the UoW (not the context)
    service = ProductService(mock_uow)

    # 3. Action
    updated_product = await service.purchase_product(product_id, quantity=purchase_quantity)

    # 4. Assertions (Check outcomes and interactions)

    # Verify domain logic was applied (stock reduced)
    assert updated_product.stock == initial_stock - purchase_quantity

    # Verify persistence was called with the updated product state
    mock_uow_ctx.products.save.assert_called_once_with(existing_product)

    # Verify transaction committed
    mock_uow_ctx.commit.assert_called_once()


@pytest.mark.asyncio
async def test_purchase_product_not_found():
    """Verifies that an appropriate error is raised if the product does not exist."""
    from unittest.mock import AsyncMock
    from uuid import uuid4
    import pytest

    # 1. Setup Mocks
    mock_uow = AsyncMock()
    mock_uow_ctx = mock_uow.__aenter__.return_value
    product_id = uuid4()

    # Configure the UoW context to return None (product not found)
    mock_uow_ctx.products.get_by_id.return_value = None

    # 2. Initialize Service
    service = ProductService(mock_uow)

    # 3. Action & Assertion
    with pytest.raises(ValueError, match="Product not found"):
        await service.purchase_product(product_id, quantity=1)

    # Verify nothing was saved or committed
    mock_uow_ctx.products.save.assert_not_called()
    mock_uow_ctx.commit.assert_not_called()


@pytest.mark.asyncio
async def test_purchase_product_insufficient_stock():
    """Verifies that the domain's ValueError is propagated if stock is low."""
    from unittest.mock import AsyncMock
    from uuid import uuid4
    from decimal import Decimal
    import pytest

    # 1. Setup Mocks
    mock_uow = AsyncMock()
    mock_uow_ctx = mock_uow.__aenter__.return_value
    product_id = uuid4()

    # Product with low stock
    existing_product = Product(
        id=product_id,
        name="LowStock",
        price=Decimal("10.00"),
        stock=1  # Only 1 in stock
    )

    # Configure get_by_id on the UoW context
    mock_uow_ctx.products.get_by_id.return_value = existing_product

    # 2. Initialize Service
    service = ProductService(mock_uow)

    # 3. Action & Assertion
    with pytest.raises(ValueError, match="Insufficient stock"):
        await service.purchase_product(product_id, quantity=5)

    # 4. Verify that save and commit were not called
    mock_uow_ctx.products.save.assert_not_called()
    mock_uow_ctx.commit.assert_not_called()

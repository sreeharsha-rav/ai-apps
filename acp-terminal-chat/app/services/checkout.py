import uuid
from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime

# -------------------------------------------------------------------------
# ACP Data Models
# -------------------------------------------------------------------------

class Address(BaseModel):
    name: Optional[str] = None
    line_one: Optional[str] = None
    line_two: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None

class Buyer(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None

class Item(BaseModel):
    id: str
    quantity: int
    title: Optional[str] = None
    image_url: Optional[str] = None

class PaymentProvider(BaseModel):
    provider: str
    supported_payment_methods: List[str]

class LineItem(BaseModel):
    id: str
    item: Item
    base_amount: int
    discount: int = 0
    subtotal: int
    tax: int = 0
    total: int

class Total(BaseModel):
    type: Literal["subtotal", "tax", "fulfillment", "total"]
    display_text: str
    amount: int

class FulfillmentOption(BaseModel):
    type: Literal["shipping", "digital"]
    id: str
    title: str
    subtotal: int
    tax: int = 0
    total: int

class Message(BaseModel):
    type: Literal["info", "error"]
    code: Optional[str] = None
    param: Optional[str] = None
    content_type: str = "plain"
    content: str

class Link(BaseModel):
    type: str
    url: str

class PaymentData(BaseModel):
    token: str
    provider: str
    billing_address: Optional[Address] = None

class Order(BaseModel):
    id: str
    checkout_session_id: str
    permalink_url: str

class CheckoutSession(BaseModel):
    id: str
    buyer: Optional[Buyer] = None
    payment_provider: Optional[PaymentProvider] = None
    status: Literal["not_ready_for_payment", "ready_for_payment", "in_progress", "completed", "canceled"]
    currency: str = "usd"
    line_items: List[LineItem] = []
    fulfillment_address: Optional[Address] = None
    fulfillment_options: List[FulfillmentOption] = []
    fulfillment_option_id: Optional[str] = None
    totals: List[Total] = []
    messages: List[Message] = []
    links: List[Link] = []
    order: Optional[Order] = None

# -------------------------------------------------------------------------
# Checkout Service
# -------------------------------------------------------------------------

class CheckoutService:
    """
    Mock implementation of Agentic Checkout Protocol.
    Stores sessions in memory for this terminal app.
    """
    def __init__(self):
        self._sessions: Dict[str, CheckoutSession] = {}

    def create_session(self, items: List[Dict[str, Any]]) -> CheckoutSession:
        """
        Creates a new checkout session.
        items: List of dicts with {"id": str, "quantity": int, "title": Optional[str], "image_url": Optional[str]}
        """
        session_id = f"cs_{uuid.uuid4().hex[:8]}"
        
        # Calculate totals (Mock logic)
        line_items = []
        subtotal_amount = 0
        for i, item_data in enumerate(items):
            # Mock price: Hash of item ID for consistency
            price = (hash(item_data["id"]) % 10000) + 1000 
            qty = item_data.get("quantity", 1)
            total = price * qty
            
            line_item = LineItem(
                id=f"li_{i}_{uuid.uuid4().hex[:4]}",
                item=Item(
                    id=item_data["id"], 
                    quantity=qty,
                    title=item_data.get("title"),
                    image_url=item_data.get("image_url")
                ),
                base_amount=total,
                subtotal=total,
                total=total
            )
            line_items.append(line_item)
            subtotal_amount += total
            
        session = CheckoutSession(
            id=session_id,
            status="not_ready_for_payment",
            line_items=line_items,
            totals=[
                Total(type="subtotal", display_text="Subtotal", amount=subtotal_amount),
                Total(type="total", display_text="Total", amount=subtotal_amount)
            ],
            payment_provider=PaymentProvider(
                 provider="stripe", 
                 supported_payment_methods=["card"]
            )
        )
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[CheckoutSession]:
        return self._sessions.get(session_id)

    def update_session(self, 
                      session_id: str, 
                      buyer: Optional[Dict[str, Any]] = None,
                      fulfillment_address: Optional[Dict[str, Any]] = None,
                      fulfillment_option_id: Optional[str] = None) -> Optional[CheckoutSession]:
        
        session = self.get_session(session_id)
        if not session:
            return None
            
        if buyer:
            session.buyer = Buyer(**buyer)
            
        if fulfillment_address:
            session.fulfillment_address = Address(**fulfillment_address)
            
            # Mock: Creating fulfillment options when address is added
            if not session.fulfillment_options:
                session.fulfillment_options = [
                    FulfillmentOption(
                        type="shipping",
                        id="ship_std",
                        title="Standard Shipping",
                        subtotal=500,
                        tax=40,
                        total=540
                    ),
                    FulfillmentOption(
                        type="shipping",
                        id="ship_exp",
                        title="Express Shipping",
                        subtotal=1500,
                        tax=120,
                        total=1620
                    )
                ]
        
        if fulfillment_option_id:
            session.fulfillment_option_id = fulfillment_option_id
            # Mock: Add shipping cost to total
            shipping_cost = 0
            tax_cost = 0
            for opt in session.fulfillment_options:
                if opt.id == fulfillment_option_id:
                    shipping_cost = opt.total
                    tax_cost = opt.tax
                    break
            
            # Recalculate totals
            subtotal = next((t.amount for t in session.totals if t.type == "subtotal"), 0)
            session.totals = [
                Total(type="subtotal", display_text="Subtotal", amount=subtotal),
                Total(type="fulfillment", display_text="Shipping", amount=shipping_cost),
                Total(type="tax", display_text="Tax", amount=tax_cost),
                Total(type="total", display_text="Total", amount=subtotal + shipping_cost)
            ]

        # Check if ready for payment
        if session.buyer and session.fulfillment_address and session.fulfillment_option_id:
             session.status = "ready_for_payment"
             
        return session

    def complete_session(self, session_id: str, payment_data: Dict[str, Any]) -> Optional[CheckoutSession]:
        session = self.get_session(session_id)
        if not session:
            return None
            
        if session.status != "ready_for_payment":
             # In robust impl, return error
             pass
             
        session.status = "completed"
        order_id = f"order_{uuid.uuid4().hex[:8]}"
        session.order = Order(
            id=order_id,
            checkout_session_id=session_id,
            permalink_url=f"https://mock-shop.com/orders/{order_id}"
        )
        return session

    def cancel_session(self, session_id: str) -> Optional[CheckoutSession]:
        session = self.get_session(session_id)
        if not session:
            return None
        session.status = "canceled"
        return session

#!/usr/bin/env python3
"""
Example 2: Modularity and Components in Software Architecture

This example demonstrates:
- Building systems from independent modules
- Component communication patterns
- Separation of concerns
- Real-world business scenario: Restaurant Order Management System

Key Concept: Modularity allows us to build complex systems by composing
smaller, independent, reusable components.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


# ============================================================================
# BUSINESS SCENARIO: Restaurant Order Management System
# ============================================================================
# A restaurant needs multiple systems working together:
# - Order taking (front of house)
# - Kitchen management (back of house)
# - Inventory tracking
# - Payment processing
# - Customer notifications
#
# Each is a separate MODULE that can be developed, tested, and maintained
# independently!


class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class MenuItem:
    """Represents a menu item"""
    id: str
    name: str
    price: float
    category: str
    preparation_time: int  # minutes


@dataclass
class Order:
    """Represents a customer order"""
    id: str
    customer_name: str
    items: List[MenuItem]
    status: OrderStatus
    created_at: datetime
    total: float


# ============================================================================
# MODULE 1: Order Management Component
# ============================================================================
# This module handles order creation and tracking.
# It doesn't know about kitchen, inventory, or payment - that's separation of concerns!

class OrderManager:
    """
    Manages customer orders.
    
    This is a COMPONENT - it has a single responsibility:
    creating and tracking orders.
    
    Architecture Principle: Single Responsibility Principle
    Each component should have one reason to change.
    """
    
    def __init__(self):
        self.orders: Dict[str, Order] = {}
        self.menu: Dict[str, MenuItem] = {
            "burger": MenuItem("burger", "Classic Burger", 12.99, "main", 15),
            "fries": MenuItem("fries", "French Fries", 4.99, "side", 5),
            "salad": MenuItem("salad", "Caesar Salad", 8.99, "main", 10),
            "drink": MenuItem("drink", "Soft Drink", 2.99, "beverage", 2),
        }
    
    def create_order(self, customer_name: str, item_ids: List[str]) -> Order:
        """Create a new order"""
        order_id = f"ORD-{len(self.orders) + 1:04d}"
        items = [self.menu[item_id] for item_id in item_ids if item_id in self.menu]
        
        order = Order(
            id=order_id,
            customer_name=customer_name,
            items=items,
            status=OrderStatus.PENDING,
            created_at=datetime.now(),
            total=sum(item.price for item in items)
        )
        
        self.orders[order_id] = order
        print(f"📝 [OrderManager] Created order {order_id} for {customer_name}")
        return order
    
    def update_order_status(self, order_id: str, status: OrderStatus):
        """Update order status"""
        if order_id in self.orders:
            self.orders[order_id].status = status
            print(f"📝 [OrderManager] Order {order_id} status: {status.value}")
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Get order by ID"""
        return self.orders.get(order_id)


# ============================================================================
# MODULE 2: Kitchen Management Component
# ============================================================================
# This module handles food preparation.
# It's completely independent - can be replaced or updated without
# affecting other modules!

class KitchenManager:
    """
    Manages kitchen operations.
    
    This component handles:
    - Receiving orders
    - Managing preparation queue
    - Notifying when food is ready
    
    Architecture Principle: Loose Coupling
    Kitchen doesn't know about orders directly - it receives notifications.
    """
    
    def __init__(self):
        self.prep_queue: List[Order] = []
        self.preparing: Dict[str, Order] = {}
    
    def receive_order(self, order: Order):
        """Receive an order for preparation"""
        print(f"👨‍🍳 [KitchenManager] Received order {order.id}")
        print(f"   Items: {', '.join(item.name for item in order.items)}")
        
        # Calculate total preparation time
        prep_time = max(item.preparation_time for item in order.items)
        print(f"   Estimated time: {prep_time} minutes")
        
        self.prep_queue.append(order)
        self._process_queue()
    
    def _process_queue(self):
        """Process orders in queue"""
        if self.prep_queue:
            order = self.prep_queue.pop(0)
            self.preparing[order.id] = order
            print(f"👨‍🍳 [KitchenManager] Started preparing order {order.id}")
    
    def mark_order_ready(self, order_id: str):
        """Mark order as ready"""
        if order_id in self.preparing:
            order = self.preparing.pop(order_id)
            print(f"👨‍🍳 [KitchenManager] Order {order.id} is READY! 🍽️")
            return order
        return None


# ============================================================================
# MODULE 3: Inventory Component
# ============================================================================
# This module tracks inventory levels.
# Independent module that can be used by multiple systems.

class InventoryManager:
    """
    Manages restaurant inventory.
    
    This component tracks:
    - Stock levels
    - Low stock alerts
    - Ingredient usage
    
    Architecture Principle: Reusability
    This component can be used by kitchen, ordering, and reporting systems.
    """
    
    def __init__(self):
        self.stock: Dict[str, int] = {
            "beef_patty": 50,
            "bun": 100,
            "lettuce": 30,
            "tomato": 25,
            "cheese": 40,
            "potato": 200,
        }
    
    def check_availability(self, item_id: str) -> bool:
        """Check if item ingredients are available"""
        # Simplified: just check if we have stock
        required_ingredients = {
            "burger": ["beef_patty", "bun", "lettuce", "tomato", "cheese"],
            "fries": ["potato"],
            "salad": ["lettuce", "tomato"],
            "drink": []  # No ingredients needed
        }
        
        ingredients = required_ingredients.get(item_id, [])
        for ingredient in ingredients:
            if self.stock.get(ingredient, 0) < 1:
                print(f"📦 [InventoryManager] ⚠️  Low stock: {ingredient}")
                return False
        return True
    
    def use_ingredients(self, item_id: str):
        """Deduct ingredients for an item"""
        required_ingredients = {
            "burger": {"beef_patty": 1, "bun": 1, "lettuce": 1, "tomato": 1, "cheese": 1},
            "fries": {"potato": 1},
            "salad": {"lettuce": 2, "tomato": 1},
        }
        
        ingredients = required_ingredients.get(item_id, {})
        for ingredient, quantity in ingredients.items():
            self.stock[ingredient] = max(0, self.stock[ingredient] - quantity)
            print(f"📦 [InventoryManager] Used {quantity}x {ingredient}")


# ============================================================================
# MODULE 4: Notification Component
# ============================================================================
# This module handles customer notifications.
# Can be swapped (SMS, email, push) without affecting other modules.

class NotificationService:
    """
    Handles customer notifications.
    
    This component demonstrates:
    - Interface-based design
    - Pluggable implementations
    - Separation of concerns
    """
    
    def send_notification(self, customer_name: str, message: str):
        """Send notification to customer"""
        print(f"📱 [NotificationService] Notifying {customer_name}: {message}")


# ============================================================================
# ORCHESTRATOR: Restaurant System
# ============================================================================
# This is the ARCHITECTURE - it composes all the modules together.
# Each module is independent, but they work together as a system.

class RestaurantSystem:
    """
    Main restaurant system that orchestrates all components.
    
    This demonstrates:
    - Component composition
    - Loose coupling
    - Dependency injection
    - System architecture
    
    Architecture Pattern: Facade Pattern
    Provides a simple interface to a complex subsystem.
    """
    
    def __init__(self):
        # Initialize all components
        self.order_manager = OrderManager()
        self.kitchen_manager = KitchenManager()
        self.inventory_manager = InventoryManager()
        self.notification_service = NotificationService()
        
        print("🏗️  [RestaurantSystem] System initialized with all components")
    
    def place_order(self, customer_name: str, item_ids: List[str]) -> Optional[Order]:
        """
        Place a new order.
        
        This method orchestrates multiple components:
        1. Check inventory
        2. Create order
        3. Send to kitchen
        4. Notify customer
        
        Architecture Principle: High Cohesion
        Related functionality is grouped together.
        """
        print(f"\n{'='*70}")
        print(f"🛒 Processing order for {customer_name}")
        print(f"{'='*70}")
        
        # Step 1: Check inventory
        for item_id in item_ids:
            if not self.inventory_manager.check_availability(item_id):
                print(f"❌ Cannot fulfill order: {item_id} out of stock")
                return None
        
        # Step 2: Create order
        order = self.order_manager.create_order(customer_name, item_ids)
        
        # Step 3: Use ingredients
        for item_id in item_ids:
            self.inventory_manager.use_ingredients(item_id)
        
        # Step 4: Send to kitchen
        self.kitchen_manager.receive_order(order)
        self.order_manager.update_order_status(order.id, OrderStatus.CONFIRMED)
        
        # Step 5: Notify customer
        self.notification_service.send_notification(
            customer_name,
            f"Order {order.id} confirmed! Total: ${order.total:.2f}"
        )
        
        return order
    
    def complete_order(self, order_id: str):
        """Mark order as ready and notify customer"""
        order = self.order_manager.get_order(order_id)
        if order:
            ready_order = self.kitchen_manager.mark_order_ready(order_id)
            if ready_order:
                self.order_manager.update_order_status(order_id, OrderStatus.READY)
                self.notification_service.send_notification(
                    ready_order.customer_name,
                    f"Your order {order_id} is ready for pickup! 🍽️"
                )


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_modularity():
    """
    Demonstrate how modularity enables building complex systems
    from simple, independent components.
    """
    print("=" * 70)
    print("EXAMPLE 2: Modularity and Components in Software Architecture")
    print("=" * 70)
    print("\n📚 Key Concepts:")
    print("   • Modularity: Building systems from independent components")
    print("   • Separation of Concerns: Each component has one responsibility")
    print("   • Loose Coupling: Components interact through well-defined interfaces")
    print("   • High Cohesion: Related functionality grouped together")
    
    # Create the restaurant system
    restaurant = RestaurantSystem()
    
    print("\n" + "=" * 70)
    print("SCENARIO: Customer Places Order")
    print("=" * 70)
    
    # Place an order - watch how multiple components work together!
    order1 = restaurant.place_order(
        customer_name="Alice",
        item_ids=["burger", "fries", "drink"]
    )
    
    print("\n" + "=" * 70)
    print("SCENARIO: Kitchen Completes Order")
    print("=" * 70)
    
    # Simulate kitchen completing the order
    if order1:
        restaurant.complete_order(order1.id)
    
    print("\n" + "=" * 70)
    print("SCENARIO: Another Customer Order")
    print("=" * 70)
    
    order2 = restaurant.place_order(
        customer_name="Bob",
        item_ids=["salad", "drink"]
    )
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT: Architecture Enables Scalability")
    print("=" * 70)
    print("""
    By using modularity:
    
    1. ✅ Each component can be developed by different teams
    2. ✅ Components can be tested independently
    3. ✅ Components can be replaced without breaking the system
    4. ✅ New features can be added as new components
    5. ✅ Components can be reused in other systems
    
    Example: The InventoryManager could be used by:
    - Restaurant system (current)
    - Warehouse management system
    - Supply chain system
    - Reporting system
    
    This is the power of modular architecture!
    """)
    
    print("\n" + "=" * 70)
    print("REAL-WORLD BUSINESS BENEFITS")
    print("=" * 70)
    print("""
    In a real restaurant business:
    
    • Team productivity: Different teams work on different modules
    • Faster development: Work in parallel on independent components
    • Easier maintenance: Fix bugs in one module without affecting others
    • Better testing: Test components in isolation
    • Technology flexibility: Use best tool for each component
    • Scalability: Scale individual components as needed
    
    All made possible by modular architecture!
    """)


if __name__ == "__main__":
    demonstrate_modularity()


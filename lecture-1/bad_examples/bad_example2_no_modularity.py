#!/usr/bin/env python3
"""
BAD EXAMPLE 2: No Modularity - Monolithic Spaghetti Code

This demonstrates what happens when you DON'T use modularity.
Compare this to example2_modularity_and_components.py to see the difference.

PROBLEMS:
1. Everything in one giant class
2. Can't test individual components
3. Can't reuse code
4. Team conflicts (everyone editing same file)
5. Bugs affect everything
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


@dataclass
class MenuItem:
    id: str
    name: str
    price: float
    category: str
    preparation_time: int


# ============================================================================
# BAD: Everything in one giant class - "God Object" anti-pattern
# ============================================================================

class RestaurantSystem:
    """
    BAD ARCHITECTURE: Monolithic class that does EVERYTHING
    
    This class violates:
    - Single Responsibility Principle
    - Separation of Concerns
    - Modularity
    
    Problems:
    1. 2000+ lines of code in one file
    2. Can't test order creation without setting up entire system
    3. Can't reuse inventory logic in warehouse system
    4. Multiple developers editing same file = merge conflicts
    5. Bug in inventory breaks order creation
    6. Can't scale individual components
    """
    
    def __init__(self):
        # BAD: All data mixed together
        self.orders: Dict[str, Dict] = {}
        self.menu: Dict[str, MenuItem] = {
            "burger": MenuItem("burger", "Classic Burger", 12.99, "main", 15),
            "fries": MenuItem("fries", "French Fries", 4.99, "side", 5),
            "salad": MenuItem("salad", "Caesar Salad", 8.99, "main", 10),
            "drink": MenuItem("drink", "Soft Drink", 2.99, "beverage", 2),
        }
        self.stock: Dict[str, int] = {
            "beef_patty": 50,
            "bun": 100,
            "lettuce": 30,
            "tomato": 25,
            "cheese": 40,
            "potato": 200,
        }
        self.kitchen_queue: List[Dict] = []
        self.preparing: Dict[str, Dict] = {}
        self.customers: Dict[str, Dict] = {}
        self.payments: Dict[str, Dict] = {}
        self.analytics: Dict[str, int] = {}
        self.notifications: List[Dict] = []
        # ... 50 more data structures
    
    def place_order(self, customer_name: str, item_ids: List[str]) -> Optional[Dict]:
        """
        BAD: This method does TOO MUCH
        
        Responsibilities mixed together:
        1. Inventory checking
        2. Order creation
        3. Inventory updates
        4. Kitchen management
        5. Customer management
        6. Notifications
        7. Analytics
        8. Payment processing
        
        Can't test one without testing all!
        """
        print(f"\n{'='*70}")
        print(f"🛒 Processing order for {customer_name}")
        print(f"{'='*70}")
        
        # BAD: Inventory logic mixed with order logic
        for item_id in item_ids:
            if item_id not in self.menu:
                print(f"❌ Invalid item: {item_id}")
                return None
            
            # BAD: Complex ingredient checking logic embedded here
            required_ingredients = self._get_ingredients_for_item(item_id)
            for ingredient in required_ingredients:
                if self.stock.get(ingredient, 0) < 1:
                    print(f"❌ Cannot fulfill order: {ingredient} out of stock")
                    return None
        
        # BAD: Order creation logic mixed with everything else
        order_id = f"ORD-{len(self.orders) + 1:04d}"
        items = [self.menu[item_id] for item_id in item_ids]
        total = sum(item.price for item in items)
        
        order = {
            'id': order_id,
            'customer_name': customer_name,
            'items': items,
            'status': OrderStatus.PENDING.value,
            'created_at': datetime.now(),
            'total': total
        }
        self.orders[order_id] = order
        
        # BAD: Inventory updates mixed with order processing
        for item_id in item_ids:
            ingredients = self._get_ingredients_for_item(item_id)
            for ingredient in ingredients:
                self.stock[ingredient] = max(0, self.stock[ingredient] - 1)
                print(f"📦 Used {ingredient}")
        
        # BAD: Kitchen management mixed with order processing
        prep_time = max(item.preparation_time for item in items)
        self.kitchen_queue.append({
            'order_id': order_id,
            'items': items,
            'prep_time': prep_time,
            'customer_name': customer_name
        })
        print(f"👨‍🍳 Sent order {order_id} to kitchen (est. {prep_time} min)")
        
        # BAD: Customer management mixed with order processing
        if customer_name not in self.customers:
            self.customers[customer_name] = {
                'orders': [],
                'total_spent': 0.0,
                'first_order_date': datetime.now()
            }
        self.customers[customer_name]['orders'].append(order_id)
        self.customers[customer_name]['total_spent'] += total
        
        # BAD: Notifications mixed with order processing
        notification = {
            'customer': customer_name,
            'message': f"Order {order_id} confirmed! Total: ${total:.2f}",
            'sent_at': datetime.now()
        }
        self.notifications.append(notification)
        print(f"📱 Notified {customer_name}: {notification['message']}")
        
        # BAD: Analytics mixed with order processing
        self.analytics['total_orders'] = self.analytics.get('total_orders', 0) + 1
        self.analytics['total_revenue'] = self.analytics.get('total_revenue', 0.0) + total
        for item in items:
            category = item.category
            self.analytics[f'{category}_orders'] = self.analytics.get(f'{category}_orders', 0) + 1
        
        # BAD: Payment processing mixed with order processing
        payment = {
            'order_id': order_id,
            'amount': total,
            'status': 'pending',
            'created_at': datetime.now()
        }
        self.payments[order_id] = payment
        
        order['status'] = OrderStatus.CONFIRMED.value
        print(f"✅ Order {order_id} confirmed!")
        
        return order
    
    def _get_ingredients_for_item(self, item_id: str) -> List[str]:
        """BAD: Helper method that should be in InventoryManager"""
        required_ingredients = {
            "burger": ["beef_patty", "bun", "lettuce", "tomato", "cheese"],
            "fries": ["potato"],
            "salad": ["lettuce", "tomato"],
            "drink": []  # No ingredients needed
        }
        return required_ingredients.get(item_id, [])
    
    def complete_order(self, order_id: str):
        """BAD: More mixed responsibilities"""
        if order_id not in self.orders:
            print(f"❌ Order {order_id} not found")
            return
        
        order = self.orders[order_id]
        
        # BAD: Kitchen logic mixed with order completion
        if order_id in self.preparing:
            del self.preparing[order_id]
        else:
            # Find in queue
            for i, queued_order in enumerate(self.kitchen_queue):
                if queued_order['order_id'] == order_id:
                    self.kitchen_queue.pop(i)
                    break
        
        # BAD: Order status update mixed with notifications
        order['status'] = OrderStatus.READY.value
        
        # BAD: Notification logic embedded here
        notification = {
            'customer': order['customer_name'],
            'message': f"Your order {order_id} is ready for pickup! 🍽️",
            'sent_at': datetime.now()
        }
        self.notifications.append(notification)
        print(f"📱 Notified {order['customer_name']}: {notification['message']}")
        
        # BAD: Payment update mixed with order completion
        if order_id in self.payments:
            self.payments[order_id]['status'] = 'completed'
    
    def get_inventory_level(self, ingredient: str) -> int:
        """BAD: Inventory method in order system"""
        return self.stock.get(ingredient, 0)
    
    def get_customer_history(self, customer_name: str) -> Dict:
        """BAD: Customer management in order system"""
        return self.customers.get(customer_name, {})
    
    def get_analytics(self) -> Dict:
        """BAD: Analytics in order system"""
        return self.analytics.copy()
    
    # ... 50 more methods doing everything!


# ============================================================================
# DEMONSTRATION: Why This Is Bad
# ============================================================================

def demonstrate_bad_architecture():
    """
    Demonstrate the problems with no modularity
    """
    print("=" * 70)
    print("BAD EXAMPLE 2: No Modularity - Monolithic Spaghetti")
    print("=" * 70)
    print("\n❌ PROBLEMS WITH THIS ARCHITECTURE:")
    print("   1. Can't test order creation without setting up entire system")
    print("   2. Can't reuse inventory logic in warehouse system")
    print("   3. Multiple developers editing same file = merge conflicts")
    print("   4. Bug in inventory breaks order creation")
    print("   5. Can't scale individual components")
    print("   6. 2000+ lines of code in one file = unmaintainable")
    
    print("\n" + "=" * 70)
    print("SCENARIO: Testing Order Creation")
    print("=" * 70)
    print("""
    To test place_order(), you need to:
    1. Set up menu items
    2. Set up inventory
    3. Set up kitchen queue
    4. Set up customer records
    5. Set up notifications
    6. Set up analytics
    7. Set up payments
    
    Result: Test setup takes 50+ lines, tests are slow, fragile!
    """)
    
    print("\n" + "=" * 70)
    print("SCENARIO: Team Development")
    print("=" * 70)
    print("""
    Team of 5 developers working on different features:
    - Developer A: Adding inventory features
    - Developer B: Adding order features
    - Developer C: Adding customer features
    - Developer D: Adding analytics
    - Developer E: Adding notifications
    
    All editing the SAME FILE!
    
    Result: Constant merge conflicts, blocking each other, slow development!
    """)
    
    print("\n" + "=" * 70)
    print("SCENARIO: Reusing Inventory Logic")
    print("=" * 70)
    print("""
    New requirement: Warehouse management system needs inventory tracking.
    
    With this architecture:
    - Can't reuse inventory logic (it's mixed with orders)
    - Must duplicate code
    - Must maintain two copies
    - Bugs fixed in one place, not the other
    
    Result: Code duplication, maintenance nightmare, inconsistent behavior!
    """)
    
    print("\n" + "=" * 70)
    print("SCENARIO: Scaling")
    print("=" * 70)
    print("""
    Business grows: Need to scale kitchen operations.
    
    With this architecture:
    - Can't scale kitchen separately
    - Must scale entire system
    - Paying for resources you don't need
    - Can't optimize individual components
    
    Result: Expensive scaling, wasted resources, poor performance!
    """)
    
    print("\n" + "=" * 70)
    print("COMPARE TO: Good Architecture (example2_modularity_and_components.py)")
    print("=" * 70)
    print("""
    With good architecture:
    
    ✅ Testing: Test each component independently (fast, reliable)
    ✅ Team work: Different teams work on different components (parallel)
    ✅ Reuse: InventoryManager can be used in warehouse system
    ✅ Scaling: Scale kitchen separately from orders
    ✅ Maintenance: Fix bugs in one component without affecting others
    
    See example2_modularity_and_components.py for the solution!
    """)


if __name__ == "__main__":
    demonstrate_bad_architecture()


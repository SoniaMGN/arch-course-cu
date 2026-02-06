#!/usr/bin/env python3
"""
Example 1: Abstraction and Interfaces in Software Architecture

This example demonstrates:
- How abstraction hides complexity
- Interface design principles
- Information hiding
- Real-world business scenario: E-commerce Payment System

Key Concept: Abstraction allows us to work with complex systems by hiding
implementation details and exposing only what's necessary.
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# BUSINESS SCENARIO: E-commerce Payment System
# ============================================================================
# Imagine you're building an e-commerce platform. You need to accept payments
# from multiple providers (Stripe, PayPal, Square) without coupling your
# code to any specific implementation. This is where abstraction shines!


class PaymentStatus(Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


@dataclass
class PaymentResult:
    """Result of a payment operation"""
    status: PaymentStatus
    transaction_id: Optional[str] = None
    message: Optional[str] = None
    amount: float = 0.0


# ============================================================================
# ABSTRACTION: Payment Interface
# ============================================================================
# This interface defines WHAT a payment processor can do, not HOW it does it.
# Any payment provider must implement these methods, but the implementation
# details are hidden.

class PaymentProcessor(ABC):
    """
    Abstract interface for payment processing.
    
    This is the ARCHITECTURAL CONTRACT - it defines the behavior that all
    payment processors must provide, regardless of their implementation.
    
    Key Principle: Clients depend on the interface, not the implementation.
    This allows us to swap payment providers without changing client code.
    """
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str, 
                      customer_info: Dict) -> PaymentResult:
        """
        Process a payment transaction.
        
        Args:
            amount: Payment amount
            currency: Currency code (USD, EUR, etc.)
            customer_info: Customer payment details
            
        Returns:
            PaymentResult with transaction status
        """
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str, 
                      amount: Optional[float] = None) -> PaymentResult:
        """
        Refund a payment.
        
        Args:
            transaction_id: Original transaction ID
            amount: Refund amount (None = full refund)
            
        Returns:
            PaymentResult with refund status
        """
        pass
    
    @abstractmethod
    def get_payment_status(self, transaction_id: str) -> PaymentStatus:
        """
        Check the status of a payment.
        
        Args:
            transaction_id: Transaction ID to check
            
        Returns:
            PaymentStatus
        """
        pass


# ============================================================================
# CONCRETE IMPLEMENTATIONS: Hidden Complexity
# ============================================================================
# These implementations hide all the complexity of communicating with
# different payment providers. The client code doesn't need to know about
# API keys, HTTP requests, webhooks, etc.

class StripePaymentProcessor(PaymentProcessor):
    """
    Stripe payment processor implementation.
    
    This hides all the complexity of:
    - Stripe API authentication
    - HTTP request handling
    - Error parsing
    - Webhook management
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._transactions = {}  # Simulated transaction storage
    
    def process_payment(self, amount: float, currency: str, 
                      customer_info: Dict) -> PaymentResult:
        """Process payment via Stripe API"""
        # In reality, this would make HTTP calls to Stripe
        # Here we simulate the complexity being hidden
        print(f"  [Stripe] Authenticating with API key: {self.api_key[:10]}...")
        print(f"  [Stripe] Creating payment intent for ${amount} {currency}")
        print(f"  [Stripe] Processing card ending in {customer_info.get('card_last4', '****')}")
        
        # Simulate API call
        transaction_id = f"stripe_{len(self._transactions) + 1}"
        self._transactions[transaction_id] = {
            'amount': amount,
            'status': PaymentStatus.SUCCESS
        }
        
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message="Payment processed successfully via Stripe",
            amount=amount
        )
    
    def refund_payment(self, transaction_id: str, 
                      amount: Optional[float] = None) -> PaymentResult:
        """Refund payment via Stripe API"""
        print(f"  [Stripe] Processing refund for {transaction_id}")
        if transaction_id in self._transactions:
            refund_amount = amount or self._transactions[transaction_id]['amount']
            return PaymentResult(
                status=PaymentStatus.REFUNDED,
                transaction_id=transaction_id,
                message=f"Refunded ${refund_amount} via Stripe",
                amount=refund_amount
            )
        return PaymentResult(
            status=PaymentStatus.FAILED,
            message="Transaction not found"
        )
    
    def get_payment_status(self, transaction_id: str) -> PaymentStatus:
        """Get payment status from Stripe"""
        return self._transactions.get(transaction_id, {}).get('status', PaymentStatus.PENDING)


class PayPalPaymentProcessor(PaymentProcessor):
    """
    PayPal payment processor implementation.
    
    Completely different implementation, but same interface!
    The client code doesn't care about the differences.
    """
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._transactions = {}
    
    def process_payment(self, amount: float, currency: str, 
                      customer_info: Dict) -> PaymentResult:
        """Process payment via PayPal API"""
        print(f"  [PayPal] Authenticating with OAuth2...")
        print(f"  [PayPal] Creating order for ${amount} {currency}")
        print(f"  [PayPal] Redirecting to PayPal checkout...")
        
        # Different API, different flow, but same interface!
        transaction_id = f"paypal_{len(self._transactions) + 1}"
        self._transactions[transaction_id] = {
            'amount': amount,
            'status': PaymentStatus.SUCCESS
        }
        
        return PaymentResult(
            status=PaymentStatus.SUCCESS,
            transaction_id=transaction_id,
            message="Payment processed successfully via PayPal",
            amount=amount
        )
    
    def refund_payment(self, transaction_id: str, 
                      amount: Optional[float] = None) -> PaymentResult:
        """Refund payment via PayPal API"""
        print(f"  [PayPal] Processing refund for {transaction_id}")
        if transaction_id in self._transactions:
            refund_amount = amount or self._transactions[transaction_id]['amount']
            return PaymentResult(
                status=PaymentStatus.REFUNDED,
                transaction_id=transaction_id,
                message=f"Refunded ${refund_amount} via PayPal",
                amount=refund_amount
            )
        return PaymentResult(
            status=PaymentStatus.FAILED,
            message="Transaction not found"
        )
    
    def get_payment_status(self, transaction_id: str) -> PaymentStatus:
        """Get payment status from PayPal"""
        return self._transactions.get(transaction_id, {}).get('status', PaymentStatus.PENDING)


# ============================================================================
# CLIENT CODE: Uses Abstraction
# ============================================================================
# This code doesn't know or care which payment provider is being used.
# It works with ANY payment processor that implements the interface.

class ECommerceStore:
    """
    E-commerce store that uses payment processors.
    
    This demonstrates the power of abstraction:
    - The store doesn't know about Stripe/PayPal internals
    - We can swap payment providers without changing this code
    - The complexity is hidden behind the interface
    """
    
    def __init__(self, payment_processor: PaymentProcessor):
        """
        Dependency Injection: We inject the payment processor.
        This makes the system flexible and testable.
        """
        self.payment_processor = payment_processor
    
    def checkout(self, cart_total: float, customer_info: Dict) -> PaymentResult:
        """
        Process checkout using the payment processor.
        
        Notice: This method doesn't care if it's Stripe, PayPal, or any
        other provider. It just uses the interface!
        """
        print(f"\n🛒 Processing checkout for ${cart_total}")
        print(f"   Customer: {customer_info.get('name', 'Guest')}")
        
        result = self.payment_processor.process_payment(
            amount=cart_total,
            currency="USD",
            customer_info=customer_info
        )
        
        if result.status == PaymentStatus.SUCCESS:
            print(f"✅ Payment successful! Transaction: {result.transaction_id}")
        else:
            print(f"❌ Payment failed: {result.message}")
        
        return result
    
    def process_refund(self, transaction_id: str, amount: Optional[float] = None):
        """Process a refund"""
        print(f"\n💰 Processing refund for transaction: {transaction_id}")
        result = self.payment_processor.refund_payment(transaction_id, amount)
        print(f"   Result: {result.message}")
        return result


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_abstraction():
    """
    Demonstrate how abstraction allows us to swap implementations
    without changing client code.
    """
    print("=" * 70)
    print("EXAMPLE 1: Abstraction and Interfaces in Software Architecture")
    print("=" * 70)
    print("\n📚 Key Concepts:")
    print("   • Abstraction hides implementation complexity")
    print("   • Interfaces define contracts between components")
    print("   • Clients depend on interfaces, not implementations")
    print("   • This enables flexibility and maintainability")
    
    print("\n" + "=" * 70)
    print("SCENARIO 1: Using Stripe Payment Processor")
    print("=" * 70)
    
    # Create Stripe processor (hides all Stripe API complexity)
    stripe = StripePaymentProcessor(api_key="sk_live_1234567890")
    store_with_stripe = ECommerceStore(stripe)
    
    # Process a payment - notice we don't see the complexity!
    store_with_stripe.checkout(
        cart_total=99.99,
        customer_info={
            'name': 'Alice',
            'email': 'alice@example.com',
            'card_last4': '4242'
        }
    )
    
    print("\n" + "=" * 70)
    print("SCENARIO 2: Switching to PayPal (No Code Changes!)")
    print("=" * 70)
    
    # Switch to PayPal - just change the processor!
    # The ECommerceStore code doesn't need to change at all!
    paypal = PayPalPaymentProcessor(
        client_id="paypal_client_123",
        client_secret="paypal_secret_456"
    )
    store_with_paypal = ECommerceStore(paypal)
    
    # Same interface, different implementation!
    store_with_paypal.checkout(
        cart_total=149.99,
        customer_info={
            'name': 'Bob',
            'email': 'bob@example.com'
        }
    )
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT: Architecture Enables Flexibility")
    print("=" * 70)
    print("""
    By using abstraction and interfaces:
    
    1. ✅ We can swap payment providers without changing business logic
    2. ✅ We can test with mock implementations
    3. ✅ We can support multiple payment providers simultaneously
    4. ✅ New developers don't need to understand payment API internals
    5. ✅ Changes to payment providers don't break our code
    
    This is the power of good software architecture!
    """)
    
    print("\n" + "=" * 70)
    print("REAL-WORLD BUSINESS BENEFITS")
    print("=" * 70)
    print("""
    In a real e-commerce business:
    
    • Negotiate better rates: Switch providers based on fees
    • Reduce risk: Support multiple providers for redundancy
    • Faster integration: New payment methods don't require refactoring
    • Better testing: Mock payment processors for unit tests
    • Team productivity: Frontend developers don't need payment API knowledge
    
    All made possible by architectural abstraction!
    """)


if __name__ == "__main__":
    demonstrate_abstraction()


#!/usr/bin/env python3
"""
BAD EXAMPLE 1: No Abstraction - Direct Coupling to Implementation

This demonstrates what happens when you DON'T use abstraction.
Compare this to example1_abstraction_and_interfaces.py to see the difference.

PROBLEMS:
1. Tightly coupled to Stripe - can't switch providers
2. Can't test without real Stripe API
3. Business logic mixed with API calls
4. Hard to add new payment methods
5. Vendor lock-in
"""

from typing import Dict, Optional
import requests  # Direct dependency on external library


# ============================================================================
# BAD: Direct coupling to Stripe API
# ============================================================================

class ECommerceStore:
    """
    BAD ARCHITECTURE: Directly calls Stripe API
    
    Problems:
    - Can't switch to PayPal without rewriting everything
    - Can't test without making real API calls
    - Business logic is mixed with API implementation
    - Every Stripe API change breaks this code
    """
    
    def __init__(self):
        # Hard-coded Stripe configuration
        self.stripe_api_key = "sk_live_1234567890"
        self.stripe_base_url = "https://api.stripe.com/v1"
        self.stripe_webhook_secret = "whsec_1234567890"
    
    def checkout(self, cart_total: float, customer_info: Dict):
        """
        BAD: Directly calls Stripe API
        
        Problems:
        1. Can't test without Stripe account
        2. Can't switch to different provider
        3. Business logic mixed with API calls
        4. Error handling is Stripe-specific
        """
        print(f"\n🛒 Processing checkout for ${cart_total}")
        print(f"   Customer: {customer_info.get('name', 'Guest')}")
        
        # BAD: Direct API call - tightly coupled!
        try:
            response = requests.post(
                f"{self.stripe_base_url}/payment_intents",
                headers={
                    "Authorization": f"Bearer {self.stripe_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "amount": int(cart_total * 100),  # Stripe uses cents
                    "currency": "usd",
                    "payment_method": customer_info.get('stripe_payment_method_id'),
                    "confirmation_method": "manual",
                    "confirm": True
                },
                timeout=30
            )
            response.raise_for_status()
            
            # BAD: Parsing Stripe-specific response
            stripe_data = response.json()
            transaction_id = stripe_data['id']
            status = stripe_data['status']
            
            if status == 'succeeded':
                print(f"✅ Payment successful! Transaction: {transaction_id}")
                return {
                    'success': True,
                    'transaction_id': transaction_id,
                    'stripe_payment_intent_id': transaction_id,  # Stripe-specific!
                    'stripe_status': status  # Stripe-specific!
                }
            else:
                print(f"❌ Payment failed: {stripe_data.get('last_payment_error', {}).get('message', 'Unknown error')}")
                return {
                    'success': False,
                    'error': stripe_data.get('last_payment_error', {}).get('message', 'Unknown error'),
                    'stripe_error_code': stripe_data.get('last_payment_error', {}).get('code')  # Stripe-specific!
                }
        
        except requests.exceptions.RequestException as e:
            # BAD: Error handling is HTTP/Stripe-specific
            print(f"❌ Stripe API error: {str(e)}")
            return {
                'success': False,
                'error': f"Stripe API error: {str(e)}"
            }
    
    def refund(self, transaction_id: str, amount: Optional[float] = None):
        """
        BAD: Direct Stripe API call for refunds
        
        Problems:
        1. Stripe-specific transaction ID format
        2. Stripe-specific refund API
        3. Can't refund PayPal transactions
        """
        print(f"\n💰 Processing refund for transaction: {transaction_id}")
        
        # BAD: Stripe-specific refund endpoint
        try:
            # First, get the payment intent
            response = requests.get(
                f"{self.stripe_base_url}/payment_intents/{transaction_id}",
                headers={"Authorization": f"Bearer {self.stripe_api_key}"}
            )
            response.raise_for_status()
            payment_intent = response.json()
            
            # Then create a refund
            refund_data = {
                "payment_intent": transaction_id
            }
            if amount:
                refund_data["amount"] = int(amount * 100)  # Stripe uses cents
            
            response = requests.post(
                f"{self.stripe_base_url}/refunds",
                headers={
                    "Authorization": f"Bearer {self.stripe_api_key}",
                    "Content-Type": "application/json"
                },
                json=refund_data
            )
            response.raise_for_status()
            
            refund = response.json()
            print(f"✅ Refund successful: {refund['id']}")
            return {
                'success': True,
                'refund_id': refund['id'],
                'stripe_refund_id': refund['id']  # Stripe-specific!
            }
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Refund failed: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }


# ============================================================================
# DEMONSTRATION: Why This Is Bad
# ============================================================================

def demonstrate_bad_architecture():
    """
    Demonstrate the problems with no abstraction
    """
    print("=" * 70)
    print("BAD EXAMPLE 1: No Abstraction - Direct Coupling")
    print("=" * 70)
    print("\n❌ PROBLEMS WITH THIS ARCHITECTURE:")
    print("   1. Can't switch to PayPal without rewriting everything")
    print("   2. Can't test without real Stripe API (costs money!)")
    print("   3. Business logic mixed with API implementation")
    print("   4. Every Stripe API change breaks this code")
    print("   5. Vendor lock-in - stuck with Stripe forever")
    
    print("\n" + "=" * 70)
    print("SCENARIO: Business wants to add PayPal")
    print("=" * 70)
    print("""
    With this architecture, you would need to:
    
    1. Duplicate ALL checkout logic for PayPal
    2. Create separate methods: checkout_stripe() and checkout_paypal()
    3. Add if/else logic everywhere to choose provider
    4. Duplicate refund logic
    5. Handle two different error formats
    6. Test two different APIs
    7. Maintain two sets of code
    
    Result: 2-3 weeks of work, code duplication, maintenance nightmare!
    """)
    
    print("\n" + "=" * 70)
    print("SCENARIO: Stripe raises their fees")
    print("=" * 70)
    print("""
    Business wants to switch to cheaper provider.
    
    With this architecture:
    - Must rewrite entire checkout system
    - Must migrate all existing transactions
    - Must update all code that uses Stripe IDs
    - Must retest everything
    - Must handle transition period
    
    Result: 3-6 months of work, $500k+ in costs, lost revenue during migration!
    """)
    
    print("\n" + "=" * 70)
    print("SCENARIO: Testing")
    print("=" * 70)
    print("""
    How do you test this code?
    
    Options:
    1. Use real Stripe API (costs money, slow, unreliable)
    2. Mock requests library (complex, brittle)
    3. Don't test (risky!)
    
    Result: Poor test coverage, bugs in production, expensive fixes!
    """)
    
    print("\n" + "=" * 70)
    print("COMPARE TO: Good Architecture (example1_abstraction_and_interfaces.py)")
    print("=" * 70)
    print("""
    With good architecture:
    
    ✅ Switch providers: Change one line of code
    ✅ Testing: Use mock implementations (free, fast, reliable)
    ✅ Multiple providers: Support all of them simultaneously
    ✅ New providers: Add new implementation, no refactoring
    ✅ Team work: Different teams work on different providers
    
    See example1_abstraction_and_interfaces.py for the solution!
    """)


if __name__ == "__main__":
    demonstrate_bad_architecture()


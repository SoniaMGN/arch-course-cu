#!/usr/bin/env python3
"""
Example 3: Architecture as Communication Tool

This example demonstrates:
- How architecture helps teams communicate
- Different views of the same system
- Architecture as documentation
- Real-world business scenario: Social Media Platform

Key Concept: Architecture is not just code - it's a communication tool
that helps teams understand, discuss, and build systems together.
"""

from typing import List, Dict, Set
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


# ============================================================================
# BUSINESS SCENARIO: Social Media Platform
# ============================================================================
# A social media platform needs to be understood by:
# - Developers (how to build it)
# - Product managers (what features exist)
# - Business stakeholders (how it works)
# - New team members (onboarding)
#
# Architecture diagrams and models help everyone speak the same language!


class UserRole(Enum):
    """User roles in the system"""
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"


@dataclass
class User:
    """Represents a user"""
    id: str
    username: str
    email: str
    role: UserRole
    created_at: datetime


@dataclass
class Post:
    """Represents a social media post"""
    id: str
    author_id: str
    content: str
    likes: int
    created_at: datetime


# ============================================================================
# VIEW 1: Logical Architecture (What the system does)
# ============================================================================
# This view shows the functional components and their relationships.
# Useful for: Product managers, business analysts, new developers

class LogicalArchitectureView:
    """
    Logical view of the system architecture.
    
    Shows WHAT the system does, not HOW it's implemented.
    This is the "business logic" view.
    """
    
    @staticmethod
    def visualize():
        """Visualize the logical architecture"""
        print("=" * 70)
        print("VIEW 1: LOGICAL ARCHITECTURE (What the system does)")
        print("=" * 70)
        print("""
        ┌─────────────────────────────────────────────────────────┐
        │              Social Media Platform                      │
        ├─────────────────────────────────────────────────────────┤
        │                                                          │
        │  ┌──────────────┐    ┌──────────────┐                  │
        │  │   User       │    │   Content    │                  │
        │  │  Management  │    │  Management  │                  │
        │  └──────┬───────┘    └──────┬───────┘                  │
        │         │                   │                           │
        │         └─────────┬──────────┘                           │
        │                   │                                     │
        │         ┌─────────▼──────────┐                         │
        │         │   Feed Generation   │                         │
        │         └─────────┬──────────┘                         │
        │                   │                                     │
        │         ┌─────────▼──────────┐                         │
        │         │  Recommendation     │                         │
        │         │      Engine         │                         │
        │         └─────────────────────┘                         │
        │                                                          │
        └─────────────────────────────────────────────────────────┘
        
        Components:
        • User Management: Handles user accounts, authentication
        • Content Management: Handles posts, comments, media
        • Feed Generation: Creates personalized feeds
        • Recommendation Engine: Suggests content to users
        """)
    
    @staticmethod
    def explain():
        """Explain what this view communicates"""
        print("\n💡 What this view tells us:")
        print("   • The main functional areas of the system")
        print("   • How components interact at a high level")
        print("   • What capabilities the system provides")
        print("   • Good for: Product planning, feature discussions")


# ============================================================================
# VIEW 2: Physical Architecture (How it's deployed)
# ============================================================================
# This view shows the actual infrastructure and deployment.
# Useful for: DevOps, infrastructure team, scalability planning

class PhysicalArchitectureView:
    """
    Physical view of the system architecture.
    
    Shows HOW the system is deployed and where components run.
    This is the "infrastructure" view.
    """
    
    @staticmethod
    def visualize():
        """Visualize the physical architecture"""
        print("\n" + "=" * 70)
        print("VIEW 2: PHYSICAL ARCHITECTURE (How it's deployed)")
        print("=" * 70)
        print("""
        ┌─────────────────────────────────────────────────────────┐
        │                    Internet                              │
        └────────────────────┬────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Load Balancer  │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
        ┌───▼───┐        ┌───▼───┐        ┌───▼───┐
        │ Web   │        │ Web   │        │ Web   │
        │Server │        │Server │        │Server │
        │ (US)  │        │ (EU)  │        │ (ASIA)│
        └───┬───┘        └───┬───┘        └───┬───┘
            │                │                │
            └────────────────┼────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
        ┌───▼───┐        ┌───▼───┐        ┌───▼───┐
        │  App  │        │  App  │        │  App  │
        │Server │        │Server │        │Server │
        └───┬───┘        └───┬───┘        └───┬───┘
            │                │                │
            └────────────────┼────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Database      │
                    │   (Replicated)   │
                    └──────────────────┘
        
        Infrastructure:
        • Load Balancer: Distributes traffic
        • Web Servers: Handle HTTP requests (3 regions)
        • App Servers: Run application logic
        • Database: Stores data (replicated for availability)
        """)
    
    @staticmethod
    def explain():
        """Explain what this view communicates"""
        print("\n💡 What this view tells us:")
        print("   • Where components are physically deployed")
        print("   • How the system scales (horizontally)")
        print("   • Infrastructure requirements")
        print("   • Good for: DevOps, capacity planning, disaster recovery")


# ============================================================================
# VIEW 3: Component Architecture (What components exist)
# ============================================================================
# This view shows the actual code components and their dependencies.
# Useful for: Developers, architects, code reviewers

class ComponentArchitectureView:
    """
    Component view of the system architecture.
    
    Shows the actual code components, classes, and their relationships.
    This is the "implementation" view.
    """
    
    @staticmethod
    def visualize():
        """Visualize the component architecture"""
        print("\n" + "=" * 70)
        print("VIEW 3: COMPONENT ARCHITECTURE (What components exist)")
        print("=" * 70)
        print("""
        ┌─────────────────────────────────────────────────────────┐
        │                    API Layer                             │
        │  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
        │  │ UserAPI  │  │ PostAPI  │  │ FeedAPI  │             │
        │  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
        └───────┼─────────────┼─────────────┼─────────────────────┘
                │             │             │
        ┌───────┼─────────────┼─────────────┼─────────────────────┐
        │       │             │             │                       │
        │  ┌────▼─────┐  ┌────▼─────┐  ┌───▼─────┐               │
        │  │ User     │  │ Post     │  │ Feed    │               │
        │  │ Service  │  │ Service  │  │ Service │               │
        │  └────┬─────┘  └────┬─────┘  └───┬─────┘               │
        │       │             │             │                       │
        │       └─────────────┼─────────────┘                       │
        │                     │                                     │
        │              ┌───────▼────────┐                          │
        │              │  Data Access    │                          │
        │              │     Layer       │                          │
        │              └───────┬────────┘                          │
        │                      │                                    │
        │              ┌───────▼────────┐                          │
        │              │   Database     │                          │
        │              │   (PostgreSQL) │                          │
        │              └────────────────┘                          │
        └───────────────────────────────────────────────────────────┘
        
        Components:
        • API Layer: REST endpoints
        • Service Layer: Business logic
        • Data Access Layer: Database interactions
        • Database: Persistent storage
        """)
    
    @staticmethod
    def explain():
        """Explain what this view communicates"""
        print("\n💡 What this view tells us:")
        print("   • What code components exist")
        print("   • How components depend on each other")
        print("   • Where to add new features")
        print("   • Good for: Development, code reviews, refactoring")


# ============================================================================
# VIEW 4: Data Flow Architecture (How data moves)
# ============================================================================
# This view shows how data flows through the system.
# Useful for: Understanding system behavior, debugging, optimization

class DataFlowArchitectureView:
    """
    Data flow view of the system architecture.
    
    Shows how data moves through the system for a specific use case.
    This is the "behavioral" view.
    """
    
    @staticmethod
    def visualize_user_creates_post():
        """Visualize data flow for creating a post"""
        print("\n" + "=" * 70)
        print("VIEW 4: DATA FLOW ARCHITECTURE (How data moves)")
        print("=" * 70)
        print("""
        Use Case: User Creates a Post
        
        1. User ──POST /api/posts──> API Layer
           │
           ├─> Validate request
           │
        2. API Layer ──> Service Layer
           │
           ├─> Check user permissions
           ├─> Validate content
           │
        3. Service Layer ──> Data Access Layer
           │
           ├─> Save post to database
           │
        4. Data Access Layer ──> Database
           │
           ├─> INSERT INTO posts...
           │
        5. Database ──> Data Access Layer
           │
           ├─> Return saved post
           │
        6. Data Access Layer ──> Service Layer
           │
           ├─> Update user's feed
           ├─> Notify followers
           │
        7. Service Layer ──> API Layer
           │
           ├─> Return success response
           │
        8. API Layer ──> User
           │
           └─> 201 Created {post_id: "123", ...}
        """)
    
    @staticmethod
    def explain():
        """Explain what this view communicates"""
        print("\n💡 What this view tells us:")
        print("   • The sequence of operations")
        print("   • Where data is transformed")
        print("   • Potential bottlenecks")
        print("   • Good for: Debugging, performance optimization, testing")


# ============================================================================
# ARCHITECTURE DOCUMENTATION GENERATOR
# ============================================================================
# In real projects, architecture views are often generated from code
# or maintained as documentation. This shows how architecture serves
# as living documentation.

class ArchitectureDocumentation:
    """
    Generates architecture documentation.
    
    In real projects, this would:
    - Generate diagrams from code
    - Keep documentation in sync with code
    - Serve as onboarding material
    - Help with decision making
    """
    
    @staticmethod
    def generate_all_views():
        """Generate all architecture views"""
        print("\n" + "=" * 70)
        print("GENERATING ARCHITECTURE DOCUMENTATION")
        print("=" * 70)
        
        LogicalArchitectureView.visualize()
        LogicalArchitectureView.explain()
        
        PhysicalArchitectureView.visualize()
        PhysicalArchitectureView.explain()
        
        ComponentArchitectureView.visualize()
        ComponentArchitectureView.explain()
        
        DataFlowArchitectureView.visualize_user_creates_post()
        DataFlowArchitectureView.explain()


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_architecture_communication():
    """
    Demonstrate how architecture serves as a communication tool
    for different stakeholders.
    """
    print("=" * 70)
    print("EXAMPLE 3: Architecture as Communication Tool")
    print("=" * 70)
    print("\n📚 Key Concepts:")
    print("   • Architecture helps teams communicate")
    print("   • Different views for different audiences")
    print("   • Architecture as living documentation")
    print("   • Shared understanding enables better decisions")
    
    # Generate all views
    ArchitectureDocumentation.generate_all_views()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT: Architecture Enables Communication")
    print("=" * 70)
    print("""
    Different stakeholders need different views:
    
    👔 Business Stakeholders:
       → Logical Architecture: "What does the system do?"
       → Data Flow: "How does a transaction work?"
    
    👨‍💻 Developers:
       → Component Architecture: "What code exists?"
       → Data Flow: "How do I add a feature?"
    
    🔧 DevOps:
       → Physical Architecture: "Where is it deployed?"
       → Data Flow: "Where are the bottlenecks?"
    
    📊 Product Managers:
       → Logical Architecture: "What features exist?"
       → Data Flow: "How does a user action work?"
    
    All views describe the SAME system, just from different perspectives!
    """)
    
    print("\n" + "=" * 70)
    print("REAL-WORLD BUSINESS BENEFITS")
    print("=" * 70)
    print("""
    In a real software business:
    
    • Faster onboarding: New team members understand system quickly
    • Better decisions: Stakeholders can discuss trade-offs visually
    • Reduced miscommunication: Everyone sees the same architecture
    • Easier planning: Product can plan features based on architecture
    • Better estimates: Developers can estimate based on component complexity
    • Documentation: Architecture diagrams serve as living documentation
    
    Architecture is not just code - it's a language for communication!
    """)


if __name__ == "__main__":
    demonstrate_architecture_communication()


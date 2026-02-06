#!/usr/bin/env python3
"""
Example 5: Evolution and Change in Software Architecture

This example demonstrates:
- How systems evolve over time
- Managing architectural changes
- Architectural drift and technical debt
- Real-world business scenario: Startup to Enterprise Growth

Key Concept: Software systems must evolve to meet changing requirements.
Good architecture makes evolution easier, while poor architecture makes
it harder and more expensive.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ============================================================================
# BUSINESS SCENARIO: Startup to Enterprise Growth
# ============================================================================
# A startup begins with a simple MVP (Minimum Viable Product).
# As it grows, the architecture must evolve to handle:
# - More users
# - More features
# - More complexity
# - More requirements
#
# This shows how architecture evolves over time!


class SystemStage(Enum):
    """Stages of system evolution"""
    MVP = "MVP - Minimum Viable Product"
    STARTUP = "Startup - Early Growth"
    SCALEUP = "Scale-up - Rapid Growth"
    ENTERPRISE = "Enterprise - Mature System"


@dataclass
class SystemMetrics:
    """Metrics for system performance"""
    users: int
    requests_per_second: int
    response_time_ms: float
    uptime_percent: float
    cost_per_month: float
    complexity_score: int  # 1-10, higher = more complex


@dataclass
class ArchitectureVersion:
    """Represents an architecture version"""
    version: str
    stage: SystemStage
    description: str
    components: List[str]
    metrics: SystemMetrics
    created_at: datetime = field(default_factory=datetime.now)


# ============================================================================
# STAGE 1: MVP (Minimum Viable Product)
# ============================================================================
# Simple, fast to build, minimal features
# Focus: Get to market quickly

class MVPArchitecture:
    """
    MVP Architecture: Simple and fast.
    
    Characteristics:
    - Single server
    - Monolithic application
    - Simple database
    - Minimal features
    
    Good for: Validating business idea
    Problems: Doesn't scale, hard to maintain long-term
    """
    
    @staticmethod
    def describe() -> ArchitectureVersion:
        """Describe MVP architecture"""
        return ArchitectureVersion(
            version="1.0",
            stage=SystemStage.MVP,
            description="Simple monolithic application on single server",
            components=[
                "Web Server (Apache)",
                "Application (Django/Python)",
                "Database (SQLite)",
                "File Storage (Local disk)"
            ],
            metrics=SystemMetrics(
                users=100,
                requests_per_second=10,
                response_time_ms=50.0,
                uptime_percent=95.0,
                cost_per_month=50.0,  # $50/month
                complexity_score=2  # Very simple
            )
        )
    
    @staticmethod
    def visualize():
        """Visualize MVP architecture"""
        print("""
        ┌─────────────────────────────────────┐
        │         Single Server               │
        │  ┌──────────┐  ┌──────────┐       │
        │  │   Web    │  │   App    │       │
        │  │  Server  │──│  (Django)│       │
        │  └──────────┘  └────┬─────┘       │
        │                     │              │
        │              ┌──────▼──────┐      │
        │              │   SQLite    │      │
        │              │  Database   │      │
        │              └─────────────┘      │
        └─────────────────────────────────────┘
        
        Pros: Simple, cheap, fast to build
        Cons: Doesn't scale, single point of failure
        """)


# ============================================================================
# STAGE 2: Startup (Early Growth)
# ============================================================================
# Add basic scaling, separate concerns
# Focus: Handle growth, improve reliability

class StartupArchitecture:
    """
    Startup Architecture: Basic scaling.
    
    Changes from MVP:
    - Separate web and app servers
    - Production database (PostgreSQL)
    - Cloud storage (S3)
    - Basic monitoring
    
    Good for: Handling initial growth
    Problems: Still monolithic, limited scalability
    """
    
    @staticmethod
    def describe() -> ArchitectureVersion:
        """Describe startup architecture"""
        return ArchitectureVersion(
            version="2.0",
            stage=SystemStage.STARTUP,
            description="Separated web/app servers, production database",
            components=[
                "Load Balancer",
                "Web Servers (2x)",
                "Application Servers (2x)",
                "Database (PostgreSQL)",
                "File Storage (S3)",
                "Monitoring (Basic)"
            ],
            metrics=SystemMetrics(
                users=10_000,
                requests_per_second=100,
                response_time_ms=80.0,
                uptime_percent=99.0,
                cost_per_month=500.0,  # $500/month
                complexity_score=4  # Moderate complexity
            )
        )
    
    @staticmethod
    def visualize():
        """Visualize startup architecture"""
        print("""
        ┌─────────────────────────────────────┐
        │      Load Balancer                 │
        └──────────┬──────────────────────────┘
                   │
        ┌──────────┼──────────┐
        │          │          │
        ┌──▼──┐  ┌──▼──┐  ┌──▼──┐
        │ Web │  │ Web │  │ App │
        │Server│  │Server│  │Server│
        └──┬──┘  └──┬──┘  └──┬──┘
           │         │        │
           └─────────┼────────┘
                     │
            ┌────────▼────────┐
            │   PostgreSQL    │
            │    Database     │
            └─────────────────┘
                   │
            ┌──────▼──────┐
            │  S3 Storage │
            └─────────────┘
        
        Pros: Better reliability, some scaling
        Cons: Still monolithic, manual scaling
        """)


# ============================================================================
# STAGE 3: Scale-up (Rapid Growth)
# ============================================================================
# Microservices, caching, CDN
# Focus: Handle rapid growth, improve performance

class ScaleUpArchitecture:
    """
    Scale-up Architecture: Microservices and optimization.
    
    Changes from Startup:
    - Microservices architecture
    - Caching layer (Redis)
    - CDN for static assets
    - Auto-scaling
    - Advanced monitoring
    
    Good for: Rapid growth, high traffic
    Problems: More complex, harder to maintain
    """
    
    @staticmethod
    def describe() -> ArchitectureVersion:
        """Describe scale-up architecture"""
        return ArchitectureVersion(
            version="3.0",
            stage=SystemStage.SCALEUP,
            description="Microservices with caching and CDN",
            components=[
                "Load Balancer",
                "API Gateway",
                "User Service (Microservice)",
                "Product Service (Microservice)",
                "Order Service (Microservice)",
                "Database (PostgreSQL, Read Replicas)",
                "Cache (Redis)",
                "CDN (CloudFront)",
                "Message Queue (RabbitMQ)",
                "Monitoring (Prometheus + Grafana)"
            ],
            metrics=SystemMetrics(
                users=1_000_000,
                requests_per_second=10_000,
                response_time_ms=120.0,
                uptime_percent=99.9,
                cost_per_month=10_000.0,  # $10k/month
                complexity_score=8  # High complexity
            )
        )
    
    @staticmethod
    def visualize():
        """Visualize scale-up architecture"""
        print("""
        ┌─────────────────────────────────────┐
        │         CDN (CloudFront)            │
        └──────────┬──────────────────────────┘
                   │
        ┌──────────▼──────────────────────────┐
        │      Load Balancer                  │
        └──────────┬──────────────────────────┘
                   │
        ┌──────────▼──────────────────────────┐
        │       API Gateway                   │
        └──────┬──────┬──────┬───────────────┘
               │      │      │
        ┌──────▼──┐ ┌─▼───┐ ┌─▼────┐
        │  User  │ │Product│ │Order │
        │Service │ │Service│ │Service│
        └────┬───┘ └───┬──┘ └───┬──┘
             │         │        │
        ┌────┼─────────┼────────┼────┐
        │    │         │        │    │
        ┌─▼──▼──┐  ┌───▼──┐  ┌──▼───┐
        │Redis  │  │PostgreSQL│ │RabbitMQ│
        │Cache  │  │(Replicas)│ │  Queue │
        └───────┘  └─────────┘ └───────┘
        
        Pros: Highly scalable, performant
        Cons: Complex, expensive, operational overhead
        """)


# ============================================================================
# STAGE 4: Enterprise (Mature System)
# ============================================================================
# Full enterprise features, global scale
# Focus: Reliability, compliance, optimization

class EnterpriseArchitecture:
    """
    Enterprise Architecture: Global scale and reliability.
    
    Changes from Scale-up:
    - Multi-region deployment
    - Advanced security
    - Compliance features
    - Disaster recovery
    - Advanced analytics
    
    Good for: Enterprise customers, global scale
    Problems: Very complex, very expensive
    """
    
    @staticmethod
    def describe() -> ArchitectureVersion:
        """Describe enterprise architecture"""
        return ArchitectureVersion(
            version="4.0",
            stage=SystemStage.ENTERPRISE,
            description="Multi-region, enterprise-grade architecture",
            components=[
                "Global Load Balancer",
                "Multi-Region API Gateways",
                "Microservices (20+ services)",
                "Databases (Multi-region, Sharded)",
                "Cache (Redis Cluster)",
                "CDN (Global)",
                "Message Queue (Kafka)",
                "Event Streaming (Kafka Streams)",
                "Search (Elasticsearch)",
                "Analytics (Data Warehouse)",
                "Security (WAF, DDoS Protection)",
                "Monitoring (Full Observability Stack)"
            ],
            metrics=SystemMetrics(
                users=100_000_000,
                requests_per_second=1_000_000,
                response_time_ms=100.0,  # Optimized
                uptime_percent=99.99,
                cost_per_month=500_000.0,  # $500k/month
                complexity_score=10  # Maximum complexity
            )
        )
    
    @staticmethod
    def visualize():
        """Visualize enterprise architecture"""
        print("""
        ┌─────────────────────────────────────────────────┐
        │         Global Load Balancer (Multi-Region)     │
        └──────┬──────────────┬──────────────┬─────────────┘
               │              │              │
        ┌──────▼──────┐ ┌────▼──────┐ ┌────▼──────┐
        │   US-East   │ │  EU-West  │ │ Asia-Pac  │
        │   Region    │ │  Region   │ │  Region   │
        │             │ │           │ │           │
        │ ┌─────────┐ │ ┌────────┐ │ ┌────────┐ │
        │ │Services │ │ │Services│ │ │Services│ │
        │ │(20+)    │ │ │(20+)   │ │ │(20+)   │ │
        │ └────┬────┘ │ └───┬────┘ │ └───┬────┘ │
        │      │      │     │      │     │      │
        │ ┌────▼────┐ │ ┌───▼───┐ │ ┌───▼───┐ │
        │ │Database │ │ │Database│ │ │Database│ │
        │ │Cluster  │ │ │Cluster│ │ │Cluster│ │
        │ └─────────┘ │ └───────┘ │ └───────┘ │
        └─────────────┴───────────┴───────────┘
        
        Pros: Global scale, enterprise features
        Cons: Very complex, very expensive
        """)


# ============================================================================
# EVOLUTION TRACKER
# ============================================================================

class ArchitectureEvolution:
    """
    Tracks how architecture evolves over time.
    
    This demonstrates:
    - How systems grow
    - When to evolve
    - Trade-offs at each stage
    - Architectural decisions
    """
    
    def __init__(self):
        self.versions: List[ArchitectureVersion] = []
    
    def add_version(self, version: ArchitectureVersion):
        """Add an architecture version"""
        self.versions.append(version)
        print(f"\n📅 {version.stage.value}")
        print(f"   Version: {version.version}")
        print(f"   {version.description}")
        print(f"   Components: {len(version.components)}")
        print(f"   Users: {version.metrics.users:,}")
        print(f"   Cost: ${version.metrics.cost_per_month:,.0f}/month")
        print(f"   Complexity: {version.metrics.complexity_score}/10")
    
    def show_evolution(self):
        """Show the evolution timeline"""
        print("\n" + "=" * 70)
        print("ARCHITECTURE EVOLUTION TIMELINE")
        print("=" * 70)
        
        for i, version in enumerate(self.versions):
            print(f"\n{i+1}. {version.stage.value}")
            print(f"   Version: {version.version}")
            print(f"   Date: {version.created_at.strftime('%Y-%m-%d')}")
            print(f"   Key Changes:")
            for component in version.components[:3]:  # Show first 3
                print(f"     • {component}")
            if len(version.components) > 3:
                print(f"     • ... and {len(version.components) - 3} more")
            print(f"   Metrics:")
            print(f"     • Users: {version.metrics.users:,}")
            print(f"     • RPS: {version.metrics.requests_per_second:,}")
            print(f"     • Response: {version.metrics.response_time_ms}ms")
            print(f"     • Uptime: {version.metrics.uptime_percent}%")
            print(f"     • Cost: ${version.metrics.cost_per_month:,.0f}/month")
    
    def analyze_evolution(self):
        """Analyze the evolution"""
        print("\n" + "=" * 70)
        print("EVOLUTION ANALYSIS")
        print("=" * 70)
        
        if len(self.versions) < 2:
            return
        
        first = self.versions[0]
        last = self.versions[-1]
        
        print(f"\n📊 Growth Metrics:")
        print(f"   Users: {first.metrics.users:,} → {last.metrics.users:,} "
              f"({last.metrics.users / first.metrics.users:,.0f}x growth)")
        print(f"   RPS: {first.metrics.requests_per_second:,} → "
              f"{last.metrics.requests_per_second:,} "
              f"({last.metrics.requests_per_second / first.metrics.requests_per_second:,.0f}x growth)")
        print(f"   Cost: ${first.metrics.cost_per_month:,.0f} → "
              f"${last.metrics.cost_per_month:,.0f} "
              f"({last.metrics.cost_per_month / first.metrics.cost_per_month:,.0f}x increase)")
        print(f"   Complexity: {first.metrics.complexity_score} → "
              f"{last.metrics.complexity_score} "
              f"({last.metrics.complexity_score - first.metrics.complexity_score:+d})")
        
        print(f"\n💡 Key Insights:")
        print(f"   • System grew {last.metrics.users / first.metrics.users:,.0f}x")
        print(f"   • Architecture evolved to handle growth")
        print(f"   • Complexity increased as features were added")
        print(f"   • Cost increased but enabled much larger scale")


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_evolution():
    """
    Demonstrate how software architecture evolves over time.
    """
    print("=" * 70)
    print("EXAMPLE 5: Evolution and Change in Software Architecture")
    print("=" * 70)
    print("\n📚 Key Concepts:")
    print("   • Systems must evolve to meet changing requirements")
    print("   • Architecture decisions impact future evolution")
    print("   • Good architecture makes evolution easier")
    print("   • Poor architecture creates technical debt")
    
    # Create evolution tracker
    evolution = ArchitectureEvolution()
    
    # Stage 1: MVP
    print("\n" + "=" * 70)
    print("STAGE 1: MVP (Month 0)")
    print("=" * 70)
    MVPArchitecture.visualize()
    mvp = MVPArchitecture.describe()
    evolution.add_version(mvp)
    
    # Stage 2: Startup
    print("\n" + "=" * 70)
    print("STAGE 2: Startup (Month 6)")
    print("=" * 70)
    print("💼 Business Growth: 100 → 10,000 users")
    print("🔧 Architecture Change: Separate servers, production database")
    StartupArchitecture.visualize()
    startup = StartupArchitecture.describe()
    evolution.add_version(startup)
    
    # Stage 3: Scale-up
    print("\n" + "=" * 70)
    print("STAGE 3: Scale-up (Month 18)")
    print("=" * 70)
    print("💼 Business Growth: 10,000 → 1,000,000 users")
    print("🔧 Architecture Change: Microservices, caching, CDN")
    ScaleUpArchitecture.visualize()
    scaleup = ScaleUpArchitecture.describe()
    evolution.add_version(scaleup)
    
    # Stage 4: Enterprise
    print("\n" + "=" * 70)
    print("STAGE 4: Enterprise (Month 36)")
    print("=" * 70)
    print("💼 Business Growth: 1,000,000 → 100,000,000 users")
    print("🔧 Architecture Change: Multi-region, enterprise features")
    EnterpriseArchitecture.visualize()
    enterprise = EnterpriseArchitecture.describe()
    evolution.add_version(enterprise)
    
    # Show evolution
    evolution.show_evolution()
    evolution.analyze_evolution()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT: Architecture Enables Evolution")
    print("=" * 70)
    print("""
    Good architecture decisions enable evolution:
    
    ✅ MVP: Simple and fast to build
       → Validates business idea quickly
    
    ✅ Startup: Basic scaling
       → Handles initial growth
    
    ✅ Scale-up: Microservices
       → Enables rapid growth
    
    ✅ Enterprise: Global architecture
       → Supports massive scale
    
    Poor architecture decisions create problems:
    
    ❌ Building enterprise architecture for MVP
       → Over-engineering, slow to market
    
    ❌ Not planning for growth
       → Technical debt, expensive rewrites
    
    ❌ Ignoring evolution
       → System becomes unmaintainable
    
    The key: Build for today, design for tomorrow!
    """)
    
    print("\n" + "=" * 70)
    print("REAL-WORLD BUSINESS LESSONS")
    print("=" * 70)
    print("""
    Real companies evolve their architecture:
    
    Amazon:
    • Started: Simple e-commerce site
    • Evolved: Microservices, AWS, global infrastructure
    • Lesson: Architecture enabled massive scale
    
    Netflix:
    • Started: DVD rental website
    • Evolved: Streaming platform, microservices, global CDN
    • Lesson: Architecture enabled business transformation
    
    Twitter:
    • Started: Simple messaging service
    • Evolved: Real-time platform, distributed systems
    • Lesson: Architecture enabled new capabilities
    
    The architecture that works for 100 users won't work
    for 100 million users. Evolution is inevitable!
    """)


if __name__ == "__main__":
    demonstrate_evolution()


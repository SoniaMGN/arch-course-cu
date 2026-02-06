#!/usr/bin/env python3
"""
Example 4: Quality Attributes and Trade-offs in Software Architecture

This example demonstrates:
- Understanding quality attributes (performance, scalability, maintainability)
- Making architectural trade-offs
- Balancing competing concerns
- Real-world business scenario: Video Streaming Service

Key Concept: Architecture involves making trade-offs between competing
quality attributes. There's no "perfect" architecture - only appropriate
ones for specific contexts.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum
import time
import random


# ============================================================================
# BUSINESS SCENARIO: Video Streaming Service
# ============================================================================
# A video streaming service must balance:
# - Performance: Fast video loading
# - Scalability: Handle millions of users
# - Cost: Infrastructure costs
# - Quality: Video quality vs bandwidth
# - Reliability: Uptime and error handling
#
# Every architectural decision involves trade-offs!


class VideoQuality(Enum):
    """Video quality levels"""
    LOW = (240, "Low bandwidth, fast loading")
    MEDIUM = (480, "Balanced quality and speed")
    HIGH = (720, "Good quality, moderate bandwidth")
    ULTRA = (1080, "Best quality, high bandwidth")
    FOURK = (2160, "Ultimate quality, very high bandwidth")


@dataclass
class Video:
    """Represents a video"""
    id: str
    title: str
    duration: int  # seconds
    file_size_mb: Dict[VideoQuality, float]  # MB per quality level


@dataclass
class StreamingMetrics:
    """Metrics for streaming performance"""
    load_time: float  # seconds
    bandwidth_used: float  # MB
    quality: VideoQuality
    buffering_events: int
    cost: float  # dollars


# ============================================================================
# ARCHITECTURE 1: Performance-Optimized (CDN + Caching)
# ============================================================================
# Prioritizes: Fast loading, low latency
# Trade-off: Higher infrastructure costs

class PerformanceOptimizedArchitecture:
    """
    Architecture optimized for performance.
    
    Strategy:
    - CDN (Content Delivery Network) for global distribution
    - Aggressive caching at multiple levels
    - Pre-loading popular content
    
    Trade-offs:
    ✅ Fast loading times
    ✅ Low latency
    ❌ Higher infrastructure costs
    ❌ More complex caching logic
    """
    
    def __init__(self):
        self.cdn_cache: Dict[str, Video] = {}
        self.edge_cache: Dict[str, Video] = {}
        self.cache_hits = 0
        self.cache_misses = 0
    
    def stream_video(self, video_id: str, user_location: str) -> StreamingMetrics:
        """Stream video with performance optimization"""
        print(f"🚀 [Performance Architecture] Streaming {video_id}")
        
        # Check edge cache first (fastest)
        if video_id in self.edge_cache:
            print("   ✅ Edge cache HIT - instant delivery")
            self.cache_hits += 1
            load_time = 0.1  # 100ms
            bandwidth = 0  # Already cached
        # Check CDN cache
        elif video_id in self.cdn_cache:
            print("   ✅ CDN cache HIT - fast delivery")
            self.cache_hits += 1
            load_time = 0.5  # 500ms
            bandwidth = 0
        else:
            print("   ❌ Cache MISS - loading from origin")
            self.cache_misses += 1
            load_time = 2.0  # 2 seconds
            bandwidth = 100  # MB
            # Cache for future requests
            self.cdn_cache[video_id] = Video(video_id, "Cached Video", 120, {})
        
        return StreamingMetrics(
            load_time=load_time,
            bandwidth_used=bandwidth,
            quality=VideoQuality.HIGH,
            buffering_events=0,
            cost=0.10  # Higher cost due to CDN
        )


# ============================================================================
# ARCHITECTURE 2: Cost-Optimized (Direct Storage)
# ============================================================================
# Prioritizes: Low infrastructure costs
# Trade-off: Slower loading, higher latency

class CostOptimizedArchitecture:
    """
    Architecture optimized for cost.
    
    Strategy:
    - Direct storage (no CDN)
    - Minimal caching
    - On-demand loading
    
    Trade-offs:
    ✅ Low infrastructure costs
    ✅ Simple architecture
    ❌ Slower loading times
    ❌ Higher latency for distant users
    """
    
    def __init__(self):
        self.storage: Dict[str, Video] = {}
    
    def stream_video(self, video_id: str, user_location: str) -> StreamingMetrics:
        """Stream video with cost optimization"""
        print(f"💰 [Cost Architecture] Streaming {video_id}")
        
        # Always load from origin (no CDN)
        print("   ⏳ Loading from origin storage...")
        load_time = 3.0  # 3 seconds (slower)
        bandwidth = 150  # MB (no caching)
        
        return StreamingMetrics(
            load_time=load_time,
            bandwidth_used=bandwidth,
            quality=VideoQuality.MEDIUM,  # Lower quality to save bandwidth
            buffering_events=1,  # More buffering
            cost=0.02  # Lower cost
        )


# ============================================================================
# ARCHITECTURE 3: Scalability-Optimized (Distributed + Load Balancing)
# ============================================================================
# Prioritizes: Handling millions of users
# Trade-off: More complex, higher operational overhead

class ScalabilityOptimizedArchitecture:
    """
    Architecture optimized for scalability.
    
    Strategy:
    - Distributed servers across regions
    - Load balancing
    - Horizontal scaling
    
    Trade-offs:
    ✅ Handles millions of concurrent users
    ✅ Can scale horizontally
    ❌ More complex architecture
    ❌ Higher operational overhead
    """
    
    def __init__(self):
        self.servers = ["us-east", "us-west", "eu-west", "asia-pacific"]
        self.load_balancer = {}
        self.active_connections = 0
    
    def stream_video(self, video_id: str, user_location: str) -> StreamingMetrics:
        """Stream video with scalability optimization"""
        print(f"📈 [Scalability Architecture] Streaming {video_id}")
        
        # Route to nearest server
        server = self._select_server(user_location)
        print(f"   🌍 Routed to {server} server")
        
        # Distribute load
        self.active_connections += 1
        print(f"   👥 Active connections: {self.active_connections}")
        
        # Simulate distributed processing
        load_time = 1.5  # Moderate load time
        bandwidth = 120  # MB
        
        return StreamingMetrics(
            load_time=load_time,
            bandwidth_used=bandwidth,
            quality=VideoQuality.HIGH,
            buffering_events=0,
            cost=0.15  # Higher cost due to multiple servers
        )
    
    def _select_server(self, user_location: str) -> str:
        """Select nearest server based on user location"""
        # Simplified: just pick a server
        return random.choice(self.servers)


# ============================================================================
# ARCHITECTURE 4: Balanced (Hybrid Approach)
# ============================================================================
# Prioritizes: Good balance of all quality attributes
# Trade-off: Not optimal in any single dimension

class BalancedArchitecture:
    """
    Architecture that balances multiple quality attributes.
    
    Strategy:
    - Moderate CDN usage
    - Smart caching
    - Regional servers for key markets
    
    Trade-offs:
    ✅ Good performance (not best)
    ✅ Reasonable cost (not cheapest)
    ✅ Decent scalability (not unlimited)
    ✅ Maintainable complexity
    """
    
    def __init__(self):
        self.cdn_enabled = True
        self.regional_servers = ["us", "eu"]  # Key markets only
        self.cache = {}
    
    def stream_video(self, video_id: str, user_location: str) -> StreamingMetrics:
        """Stream video with balanced approach"""
        print(f"⚖️  [Balanced Architecture] Streaming {video_id}")
        
        # Smart caching: cache popular content
        if video_id in self.cache:
            print("   ✅ Cache HIT")
            load_time = 0.8
            bandwidth = 0
        else:
            print("   ⏳ Loading from regional server")
            load_time = 2.0
            bandwidth = 130
            # Cache if popular
            if random.random() > 0.5:  # 50% cache popular content
                self.cache[video_id] = True
        
        return StreamingMetrics(
            load_time=load_time,
            bandwidth_used=bandwidth,
            quality=VideoQuality.HIGH,
            buffering_events=0,
            cost=0.06  # Moderate cost
        )


# ============================================================================
# QUALITY ATTRIBUTE ANALYSIS
# ============================================================================

class ArchitectureAnalyzer:
    """
    Analyzes different architectures based on quality attributes.
    
    This demonstrates how architects evaluate trade-offs.
    """
    
    @staticmethod
    def compare_architectures():
        """Compare different architectural approaches"""
        print("\n" + "=" * 70)
        print("ARCHITECTURE COMPARISON: Quality Attributes Trade-offs")
        print("=" * 70)
        
        architectures = {
            "Performance-Optimized": PerformanceOptimizedArchitecture(),
            "Cost-Optimized": CostOptimizedArchitecture(),
            "Scalability-Optimized": ScalabilityOptimizedArchitecture(),
            "Balanced": BalancedArchitecture(),
        }
        
        print("\n" + "-" * 70)
        print("SCENARIO: Stream video to 1 million users")
        print("-" * 70)
        
        results = {}
        for name, arch in architectures.items():
            print(f"\n📊 Testing {name} Architecture:")
            metrics = arch.stream_video("video123", "us-east")
            results[name] = metrics
        
        print("\n" + "=" * 70)
        print("COMPARISON RESULTS")
        print("=" * 70)
        print(f"{'Architecture':<25} {'Load Time':<12} {'Cost/User':<12} {'Quality':<12}")
        print("-" * 70)
        
        for name, metrics in results.items():
            print(f"{name:<25} {metrics.load_time:<12.2f} ${metrics.cost:<11.2f} {metrics.quality.name}")
        
        print("\n" + "=" * 70)
        print("TRADE-OFF ANALYSIS")
        print("=" * 70)
        print("""
        Performance-Optimized:
        ✅ Best load times (0.1-0.5s)
        ❌ Highest cost ($0.10/user)
        ✅ Best user experience
        → Good for: Premium service, low latency requirements
        
        Cost-Optimized:
        ✅ Lowest cost ($0.02/user)
        ❌ Slowest load times (3s)
        ❌ More buffering
        → Good for: Budget service, cost-sensitive markets
        
        Scalability-Optimized:
        ✅ Handles millions of users
        ✅ Good performance (1.5s)
        ❌ Higher cost ($0.15/user)
        ❌ Complex operations
        → Good for: Large scale, global service
        
        Balanced:
        ✅ Good performance (0.8-2s)
        ✅ Reasonable cost ($0.06/user)
        ✅ Maintainable
        → Good for: Most businesses, general purpose
        """)


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demonstrate_quality_tradeoffs():
    """
    Demonstrate how architects make trade-offs between quality attributes.
    """
    print("=" * 70)
    print("EXAMPLE 4: Quality Attributes and Trade-offs")
    print("=" * 70)
    print("\n📚 Key Concepts:")
    print("   • Quality attributes: Performance, Scalability, Cost, Reliability")
    print("   • Trade-offs: Improving one often hurts another")
    print("   • Context matters: Right architecture depends on requirements")
    print("   • No perfect solution: Only appropriate ones for specific needs")
    
    # Compare architectures
    ArchitectureAnalyzer.compare_architectures()
    
    print("\n" + "=" * 70)
    print("KEY INSIGHT: Architecture is About Trade-offs")
    print("=" * 70)
    print("""
    Every architectural decision involves trade-offs:
    
    🚀 Performance vs Cost:
       Fast systems cost more (CDN, caching, premium infrastructure)
    
    📈 Scalability vs Complexity:
       Highly scalable systems are more complex to build and operate
    
    💰 Cost vs Quality:
       Lower costs often mean lower quality or slower performance
    
    🔧 Flexibility vs Performance:
       Flexible systems may be slower than optimized ones
    
    The architect's job is to:
    1. Understand business requirements
    2. Identify quality attribute priorities
    3. Make informed trade-offs
    4. Document decisions and rationale
    """)
    
    print("\n" + "=" * 70)
    print("REAL-WORLD BUSINESS DECISIONS")
    print("=" * 70)
    print("""
    Real businesses make these trade-offs daily:
    
    Netflix:
    • Chose: Performance + Scalability
    • Trade-off: Higher infrastructure costs
    • Result: Premium service, global reach
    
    YouTube:
    • Chose: Scalability + Cost optimization
    • Trade-off: Some performance compromises
    • Result: Free service, massive scale
    
    Vimeo:
    • Chose: Quality + Performance
    • Trade-off: Higher costs, smaller scale
    • Result: Premium quality, niche market
    
    Each made different trade-offs based on their business model!
    """)


if __name__ == "__main__":
    demonstrate_quality_tradeoffs()


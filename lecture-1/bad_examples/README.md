# Bad Architecture Examples

This directory contains examples of **BAD architecture** to demonstrate what happens when you don't follow architectural principles.

## Purpose

These examples show:
1. ❌ **What NOT to do** - Anti-patterns and bad practices
2. 💥 **Real consequences** - Problems that arise from bad architecture
3. 📊 **Cost impact** - Time and money wasted

## Examples

### `bad_example1_no_abstraction.py`
**Problem**: Direct coupling to implementation (Stripe API)

**Consequences**:
- Can't switch payment providers
- Can't test without real API
- Vendor lock-in
- Code duplication

**Compare to**: `../example1_abstraction_and_interfaces.py`

### `bad_example2_no_modularity.py`
**Problem**: Monolithic "God Object" that does everything

**Consequences**:
- Can't test individual components
- Team conflicts (everyone editing same file)
- Can't reuse code
- Can't scale components independently

**Compare to**: `../example2_modularity_and_components.py`

## Running the Examples

```bash
# See what bad architecture looks like
python3 bad_example1_no_abstraction.py
python3 bad_example2_no_modularity.py
```

## Key Lessons

1. **Abstraction matters**: Without it, you're locked into implementations
2. **Modularity matters**: Without it, you can't test, scale, or maintain
3. **Architecture matters**: Bad decisions cost time and money

## Real-World Impact

These patterns lead to:
- **$500k - $2M** in migration costs
- **3-6 months** of development time wasted
- **Lost revenue** during transitions
- **Team productivity** losses
- **Failed projects**

See `../TUTORIAL.md` for detailed explanations and comparisons.


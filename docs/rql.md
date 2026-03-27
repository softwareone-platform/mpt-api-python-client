# RQL Query Builder

`RQLQuery` is a fluent, type-safe builder for [Resource Query Language](https://doc.mpt.softwareone.com)
(RQL) filter expressions. RQL is used across the MPT API to express filters, sorting, and
field selection in a single, composable query string that the service mixins understand.

## Builder Usage

```python
from mpt_api_client import RQLQuery

query = RQLQuery(status="active", product__id="PRD-123")
```

Instantiate `RQLQuery` with keyword arguments that mimic the API field names (use `__` to
nest properties). The builder instance can then be passed to service mixins or chained
via `QueryableMixin` helpers.

## QueryableMixin Integration

Service mixins such as `QueryableMixin` expose methods like `filter()`, `order_by()`, and
`select()` which accept `RQLQuery` instances. Each call returns a new `QueryableMixin` that
appends filters immutably, allowing expression composition without shared mutation.

## Composing Multiple Filters

You can build complex predicates by joining queries with `&` (AND), `|` (OR), and `~` (NOT):

```python
from mpt_api_client import MPTClient, RQLQuery

client = MPTClient()
products = client.catalog.products

target_ids = RQLQuery("id").in_([
    "PRD-123-456",
    "PRD-789-012",
])
active = RQLQuery(status="active")
vendor = RQLQuery("vendor.name").eq("Microsoft")

query = target_ids & active & vendor

result = products.filter(query).order_by("-audit.updated.at").select("id", "name")
for product in result.iterate():
    print(product.id, product.name)
```

You can mix AND and OR to widen the match set while keeping base filters applied:

```python
base = RQLQuery(status="active")
cheap = RQLQuery("price.amount").lt(50)
featured = RQLQuery("tags").in_(["featured", "bundle"])

query = base & (cheap | featured)

filtered = products.filter(query)
```

Filters stay immutable: repeated `filter()` calls stack with AND by default.

```python
recent = RQLQuery("updated_at").ge("2024-01-01")
has_docs = RQLQuery("documents.id").in_(["DOC-123", "DOC-456"])

stacked = products.filter(recent).filter(has_docs)

combined = recent & has_docs
assert str(stacked.query_state.filter) == str(combined)
```







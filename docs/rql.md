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
from mpt_api_client import MPTClient, BearerTokenAuthentication, RQLQuery

client = MPTClient.from_config(
    authentication=BearerTokenAuthentication("<token>"),
    base_url="https://api.s1.show/public",
)
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

## Value Encoding

A filter value has to survive two independent layers, and the builder handles both.

### The URL query string

`&` and `#` are delimiters in a query string, so a value carrying them must be
percent-encoded or it never arrives intact: `&` splits the filter into two query parameters,
and everything after a `#` becomes the URL fragment and never leaves the client at all. `+`
decodes to a space. A `%` followed by two hex digits is read as an escape and silently
mis-decodes, though a standalone `%` is tolerated. The builder percent-encodes every value
and field name it renders:

```python
RQLQuery(name="H&R Block")
# eq(name,'H%26R%20Block')
```

### The RQL expression

`,` `;` `|` `=` `(` `)` are RQL operators, not data. They are inert inside a string
literal, which is why the builder always quotes string values — that, not percent-encoding,
is what keeps them safe.

The one character a literal cannot carry is its own delimiter, and percent-encoding does
not help: the server decodes the query parameter *before* parsing the expression, so `%27`
reaches the parser as a bare `'` and ends the literal early. RQL accepts either `'` or `"`
as the delimiter, so the builder chooses per value:

```python
RQLQuery(name="Fisher & Sauls, P. A.")  # eq(name,'Fisher%20%26%20Sauls%2C%20P.%20A.')
RQLQuery(name="Maria's Super Store")  # eq(name,"Maria%27s%20Super%20Store")
```

A value containing **both** quote characters cannot be expressed by any RQL literal, so the
builder raises `ValueError` rather than sending a request that fails server-side:

```python
RQLQuery(name='Standard & Poor\'s "AAA" rating')
# ValueError: An RQL value cannot contain both a single and a double quote, ...
```

### Deliberate exceptions

- `*` stays literal, because it is the `like`/`ilike` wildcard rather than data. A value
  cannot therefore carry a literal `*`.
- The dot in a nested field path stays literal, because it is the nesting separator.
  `RQLQuery("vendor.name")` still targets the nested `name` field.

### Escape hatch

`RQLQuery.from_string()` takes an expression verbatim and neither encodes nor quotes
anything, so interpolating unvalidated input into it reintroduces every failure above —
including letting a value close its literal and append its own RQL operators. Prefer the
builder for anything carrying a value.

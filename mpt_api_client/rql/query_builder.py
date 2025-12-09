import datetime as dt
from decimal import Decimal
from typing import Any, Self, override

from mpt_api_client.rql import constants

Numeric = int | float | Decimal

QueryValue = str | bool | dt.date | dt.datetime | Numeric


def parse_kwargs(query_dict: dict[str, QueryValue]) -> list[str]:  # noqa: WPS231
    """
    Parse keyword arguments into RQL query expressions.

    Converts a dictionary of field lookups and values into a list of RQL query
    expressions. Supports field lookups with operators (e.g., 'field__eq', 'field__in')
    and handles nested fields using dot notation.

    Args:
        query_dict (dict): Dictionary where keys are field lookups (optionally with
            operators separated by '__') and values are the comparison values.

    Returns:
        list[str]: List of RQL query expression strings ready for use in queries.

    Examples:
        parse_kwargs({'name': 'John', 'age__gt': 25})
        ['eq(name,John)', 'gt(age,25)']

        parse_kwargs({'status__in': ['active', 'pending']})
        ['in(status,(active,pending))']
    """
    query = []
    for lookup, value in query_dict.items():
        tokens = lookup.split("__")
        if len(tokens) == 1:
            field = tokens[0]
            str_value = rql_encode("eq", value)
            query.append(f"eq({field},{str_value})")
            continue
        op = tokens[-1]
        if op not in constants.KEYWORDS:
            field = ".".join(tokens)
            str_value = rql_encode("eq", value)
            query.append(f"eq({field},{str_value})")
            continue
        field = ".".join(tokens[:-1])
        if op in constants.COMP or op in constants.SEARCH:
            str_value = rql_encode(op, value)
            query.append(f"{op}({field},{str_value})")
            continue
        if op in constants.LIST:
            str_value = rql_encode(op, value)
            query.append(f"{op}({field},({str_value}))")
            continue

        cmpop = "eq" if value is True else "ne"
        expr = "null()" if op == constants.NULL else "empty()"
        query.append(f"{cmpop}({field},{expr})")

    return query


def query_value_str(value: QueryValue) -> str:
    """Converts a value to string for use in RQL queries."""
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"

    if isinstance(value, dt.date | dt.datetime):
        return value.isoformat()
    # Matching: if isinstance(value, int | float | Decimal):
    return str(value)


def rql_encode(op: str, value: Any) -> str:
    """
    Encode a value for use in RQL queries based on the operator type.

    Converts Python values to their RQL string representation. For non-list operators,
    handles strings, booleans, numbers, dates, and datetimes. For list operators,
    joins list/tuple values with commas.

    Args:
        op (str): The RQL operator being used (e.g., 'eq', 'in', 'like').
        value: The value to encode. Can be str, bool, int, float, Decimal,
            date, datetime, list, or tuple.

    Returns:
        str: The RQL-encoded string representation of the value.

    Raises:
        TypeError: If the operator doesn't support the given value type.

    Examples:
        rql_encode('eq', 'hello')
        'hello'

        rql_encode('eq', True)
        'true'

        rql_encode('in', ['a', 'b', 'c'])
        'a,b,c'
    """
    if op not in constants.LIST and isinstance(value, QueryValue):
        return query_value_str(value)
    if op in constants.LIST and isinstance(value, list | tuple | set):
        return ",".join(str(el) for el in value)

    raise TypeError(f"the `{op}` operator doesn't support the {type(value)} type.")


class RQLQuery:
    """
    Helper class to construct complex RQL queries.

    Examples:
        Creating a query
            rql = RQLQuery(field='value', field2__in=('v1', 'v2'), field3__empty=True)

        Joining queries
            rql = (
                RQLQuery().n('field').eq('value')
                & RQLQuery().n('field2').anyof(('v1', 'v2'))
                & RQLQuery().n('field3').empty(True)
            )

        Using attributes
            rql = RQLQuery().field.eq('value')
                & RQLQuery().field2.anyof(('v1', 'v2'))
                & r.field3.empty(True)

        Comparation
            rql = RQLQuery("field").eq("value")

        The R object support the bitwise operators `&`, `|` and `~`.

        Nested fields can be expressed using dot notation:
            rql = RQLQuery().n('nested.field').eq('value')
            rql = RQLQuery().nested.field.eq('value')
    """

    OP_AND = "and"
    OP_OR = "or"
    OP_ANY = "any"
    OP_ALL = "all"
    OP_EXPRESSION = "expr"

    def __init__(  # noqa: WPS211
        self,
        namespace_: str | None = None,  # noqa: WPS120
        **kwargs: QueryValue,
    ) -> None:
        self.op: str = self.OP_EXPRESSION
        self.children: list[RQLQuery] = []
        self.negated: bool = False
        self.expr: str | None = None
        self._path: list[str] = []
        self._field: str | None = None
        if namespace_:
            self.n(namespace_)
        if len(kwargs) == 1:
            self.op = self.OP_EXPRESSION
            self.expr = parse_kwargs(kwargs)[0]
        if len(kwargs) > 1:
            self.op = self.OP_AND
            for token in parse_kwargs(kwargs):
                self.children.append(self.new(expr=token))

    @classmethod
    def new(
        cls,
        expr: str | None = None,
        *,
        negated: bool = False,
        op: str | None = None,
        children: list["RQLQuery"] | set["RQLQuery"] | None = None,
    ) -> Self:
        """Create a new RQLQuery object from a expression or from a set of op and children."""
        if isinstance(children, set):
            children = list(children)
        query = cls()
        query.op = op or cls.OP_EXPRESSION
        query.children = children or []
        query.negated = negated
        query.expr = expr
        return query

    @classmethod
    def from_string(cls, query_string: str) -> Self:
        """Create a new RQLQuery object from a string."""
        return cls.new(expr=query_string)

    def __len__(self) -> int:
        if self.op == self.OP_EXPRESSION:
            if self.expr:
                return 1
            return 0
        return len(self.children)

    def __bool__(self) -> bool:
        return bool(self.children) or bool(self.expr)

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return False
        return (
            self.op == other.op
            and self.children == other.children
            and self.negated == other.negated
            and self.expr == other.expr
        )

    @override
    def __hash__(self) -> int:
        return hash(
            (
                self.op,
                self.expr,
                self.negated,
                *(hash(value) for value in self.children),
            ),
        )

    @override
    def __repr__(self) -> str:
        if self.op == self.OP_EXPRESSION:
            return f"<RQLQuery({self.op}) {self.expr}>"
        return f"<RQLQuery({self.op})>"

    def __and__(self, other: object) -> Self:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._join(other, self.OP_AND)

    def __or__(self, other: object) -> Self:
        if not isinstance(other, type(self)):
            return NotImplemented
        return self._join(other, self.OP_OR)

    def __invert__(self) -> Self:
        inverted_query = self.new(
            op=self.OP_AND,
            expr=self.expr,
            negated=True,
        )
        inverted_query._append(self)  # noqa: SLF001
        return inverted_query

    def __getattr__(self, name: str) -> Self:
        return self.n(name)

    @override
    def __str__(self) -> str:
        return self._to_string(self)

    def any(self) -> Self:
        """Any nested objects have to match the filter condition.

        Returns:
            RQLQuery: RQLQuery with new condition

        Examples:
            RQLQuery(saleDetails__orderQty__gt=11).any()
            will result: any(saleDetails,orderQty=11)
        """
        return self.new(op=self.OP_ANY, children=[self])

    def all(self) -> Self:
        """All nested objects have to match the filter condition.

        Returns:
            RQLQuery: RQLQuery with new condition

        Example:
            RQLQuery(saleDetails__orderQty__gt=1).all()
        """
        return self.new(op=self.OP_ALL, children=[self])

    def n(self, name: str) -> Self:  # noqa: WPS111
        """Set the current field for this `RQLQuery` object.

        Args:
            name: Name of the field.

        Examples:
            RQLQuery().n('field')
            RQLQuery().n('field.nested.field')
        """
        if self._field:
            raise AttributeError("Already evaluated")

        self._path.extend(name.split("."))
        return self

    def ne(self, value: QueryValue) -> Self:
        """Check if the value is NOT EQUAL to the field this `RQLQuery` object refers to.

        Args:
            value: The value to which compare the field.

        Examples:
            RQLQuery().field.ne(value)
        """
        return self._bin("ne", value)

    def eq(self, value: QueryValue) -> Self:
        """Check if the value is EQUAL to the field this `RQLQuery` object refers to.

        Args:
            value: The value to which compare the field.

        Examples:
            RQLQuery().field.eq(value)
        """
        return self._bin("eq", value)

    def lt(self, value: QueryValue) -> Self:
        """Check if the value is less than the field this `RQLQuery` object refers to.

        Args:
            value: The value to which compare the field.

        Examples:
            RQLQuery().field.lt(value)
        """
        return self._bin("lt", value)

    def le(self, value: QueryValue) -> Self:
        """Check if the value is less than or equal to the field this `RQLQuery` object refers to.

        Args:
            value (str): The value to which compare the field.

        Examples:
            RQLQuery().field.le(value)
        """
        return self._bin("le", value)

    def gt(self, value: QueryValue) -> Self:
        """Check if the value is greater than the field this `RQLQuery` object refers to.

        Args:
            value: The value to which compare the field.

        Examples:
            RQLQuery().field.gt(value)
        """
        return self._bin("gt", value)

    def ge(self, value: QueryValue) -> Self:
        """Check if the value is greater or equal than the field RQL refers to.

        Args:
            value: The value to which compare the field.

        Examples:
            RQLQuery().field.ge(value)
        """
        return self._bin("ge", value)

    def out(self, value: list[QueryValue]) -> Self:
        """Check if the `RQLQuery` objects refers it is NOT in the list of values.

        Args:
            value: The list of values to which compare the field.

        Examples:
            RQLQuery().field.out(['value1', 'value2'])
        """
        return self._list("out", value)

    def in_(self, value: list[QueryValue]) -> Self:
        """Check if the `RQLQuery` objects refers it is in the list of values.

        Args:
            value: The list of values to which compare the field.

        Examples:
            RQLQuery().field.in_(['value1', 'value2'])
        """
        return self._list("in", value)

    def oneof(self, value: list[QueryValue]) -> Self:
        """
        Apply the `in` operator to the field this `RQLQuery` object refers to.

        Args:
            value: The list of values to which compare the field.

        Examples:
            RQLQuery().field.oneof(['value1', 'value2'])
        """
        return self._list("in", value)

    def null(self, value: bool) -> Self:  # noqa: FBT001
        """Applies the `null` operator to the field this `RQLQuery` object refers to.

        Args:
            value: True to check for null, False to check for not null.

        Examples:
            To check if field is null:
                RQLQuery().field.null()

            To check if field is not null:
                RQLQuery().field.not_null()
        """
        return self._bool("null", value)

    def empty(self, value: bool = True) -> Self:  # noqa: FBT001 FBT002
        """Apply the `empty` operator to the field this `RQLQuery` object refers to.

        Args:
            value: True to check for empty, False to check for not empty.

        Examples:
            To check if field is empty:
                RQLQuery().field.empty()

            For not empty:
                RQLQuery().field.empty(False) or RQLQuery().field.not_empty()
        """
        return self._bool("empty", value)

    def not_empty(self) -> Self:
        """Apply the `not_empty` operator to the field this `RQLQuery` object refers to.

        Examples:
            To check if the object `RQLQuery` refers to is like value:
                RQLQuery().field.not_empty()
        """
        return self._bool("empty", value=False)

    def like(self, value: QueryValue) -> Self:
        """Apply the `like` operator to the field this `RQLQuery` object refers to.

        Args:
            value: The value to which compare the field.

        Examples:
            To check if the object `RQLQuery` refers to is like value:
                RQLQuery().field.like(value)
        """
        return self._bin("like", value)

    def ilike(self, value: QueryValue) -> Self:
        """
        Apply the `ilike` operator to the field this `RQLQuery` object refers to.

        Args:
            value: The value to which compare the field.

        Examples:
            RQLQuery().field.ilike(value)
        """
        return self._bin("ilike", value)

    def _bin(self, op: str, value: QueryValue) -> Self:
        self._field = ".".join(self._path)
        value = rql_encode(op, value)
        self.expr = f"{op}({self._field},{value})"
        return self

    def _list(self, op: str, value_list: list[QueryValue]) -> Self:
        self._field = ".".join(self._path)
        encoded_list = rql_encode(op, value_list)
        self.expr = f"{op}({self._field},({encoded_list}))"
        return self

    def _bool(self, expr: str, value: QueryValue) -> Self:
        self._field = ".".join(self._path)
        if bool(value) is False:
            self.expr = f"ne({self._field},{expr}())"
            return self
        self.expr = f"eq({self._field},{expr}())"
        return self

    def _to_string(self, query: "RQLQuery") -> str:
        if query.expr:
            if query.negated:
                return f"not({query.expr})"
            return query.expr
        tokens = [self._to_string(query) for query in query.children]
        if not tokens:
            return ""
        str_tokens = ",".join(tokens)
        if query.negated:
            return f"not({query.op}({str_tokens}))"
        return f"{query.op}({str_tokens})"

    def _copy(self, other: "RQLQuery") -> Self:
        return self.new(
            op=other.op,
            children=other.children.copy(),
            expr=other.expr,
        )

    def _join(self, other: "RQLQuery", op: str) -> Self:
        if self == other:
            return self._copy(self)
        if not other:
            return self._copy(self)
        if not self:
            return self._copy(other)

        query = self.new(op=op)
        query._append(self)  # noqa: SLF001
        query._append(other)  # noqa: SLF001
        return query

    def _append(self, query: "RQLQuery") -> "RQLQuery" | Self:
        if query in self.children:
            return query
        single_operation = len(query) == 1 and query.op != self.OP_EXPRESSION
        if (query.op == self.op or single_operation) and not query.negated:
            self.children.extend(query.children)
            return self

        self.children.append(query)
        return self

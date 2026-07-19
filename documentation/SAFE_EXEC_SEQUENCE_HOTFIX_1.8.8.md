# Safe-Exec Sequence-Unpacking Hotfix — v1.8.8

## Confirmed failure

Frappe 15.83 compiles API Server Scripts through RestrictedPython. Its
`get_safe_globals()` exposes:

```text
_iter_unpack_sequence_
```

but does not expose:

```text
_unpack_sequence_
```

RestrictedPython uses `_unpack_sequence_` for normal multi-target assignment:

```python
a, b = helper()
```

That caused the Criterion 7 failure:

```text
NameError: name '_unpack_sequence_' is not defined
```

The failing statement was the three-value assignment returned by
`metric_required_fields()`.

## Fix

Affected scripts now store the helper result in one variable and access values
by index:

```python
result = metric_required_fields(metric, doctype)
resolved_fields = result[0]
missing = result[1]
resolved_conditions = result[2]
```

The same compatibility review was applied to:

- Criterion 1
- Criterion 2
- Criterion 3
- Criterion 5
- Criterion 6
- Criterion 7

Criterion 5 also no longer calls `frappe.has_permission`, which is not exposed
in the same Frappe safe-exec namespace. Its source loader now relies on the
permission-aware `frappe.get_list` call and classifies permission exceptions.

## Unchanged

- API method names
- payload format
- policy registries
- source registries
- metric definitions
- response contract
- dashboard layout
- chart logic

## Deployment

Replace the six affected API Server Script bodies. Replacing the Custom HTML
Block is optional for this hotfix and only updates the displayed version.

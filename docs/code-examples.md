# Code Examples

## Python

```python title="add_numbers.py"
def add_numbers(a, b):
    """Returns the sum of two numbers."""
    return a + b
```

## JavaScript

```javascript
function multiplyNumbers(a, b) {
    // Returns the product of two numbers.
    return a * b;
}
```

## superfences extension

```yaml
    - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
    - pymdownx.inlinehilite
    - pymdownx.snippets
    - pymdownx.superfences

```

## Java

```java linenums="1"
    public class Example {
        public static void main(String[] args) {
            System.out.println("Hello, World!");
        }
    }
```

This will enable enhanced code block support with syntax highlighting and other features provided by the `pymdownx.superfences` extension.

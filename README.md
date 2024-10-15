# pure python


```
import pure

# Example usage
class Example:
    def pure_method(self, a, b):
        return a + b

    def impure_method(self, item):
        self.some_list.append(item)

# Test the purity checker
print(pure.is_method_pure(Example.pure_method))
print(pure.is_method_pure(Example.impure_method))

```

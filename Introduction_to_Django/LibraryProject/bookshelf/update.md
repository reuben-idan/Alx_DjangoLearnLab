# Update the Book title

```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(book.title)
```

# Expected Output

```
Nineteen Eighty-Four
```

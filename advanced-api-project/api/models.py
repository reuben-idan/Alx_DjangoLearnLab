from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Author(models.Model):
    """
    Model representing an author of books.
    """
    name = models.CharField(
        max_length=200,
        help_text="Enter the author's full name"
    )
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(
        max_length=200,
        help_text="Enter the book title"
    )
    publication_year = models.IntegerField(
        help_text="Enter the year the book was published"
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
        help_text="Select the book's author"
    )
    
    class Meta:
        ordering = ['title', 'publication_year']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'], 
                name='unique_book_author'
            )
        ]
    
    def clean(self):
        """
        Validate that the publication year is not in the future.
        """
        current_year = timezone.now().year
        if self.publication_year > current_year:
            raise ValidationError(
                {'publication_year': 'Publication year cannot be in the future.'}
            )
    
    def save(self, *args, **kwargs):
        """
        Override save to call full_clean for validation.
        """
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        """String for representing the Model object."""
        return f"{self.title} ({self.publication_year})"

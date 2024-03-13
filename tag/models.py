from django.db import models
# from django.contrib.contenttypes.models import ContentType
# from django.contrib.contenttypes.fields import GenericForeignKey

from utils.slug import new_slug


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Nome',
        max_length=50,
    )

    slug = models.SlugField(
        unique=True
    )

    # # Aqui ira começar os campos para relações genéricas

    # # Representa o model que sera encaixado aqui
    # content_type = models.ForeignKey(
    #     ContentType, on_delete=models.CASCADE
    # )
    # # Representa o id da linha do model descrito acima
    # object_id = models.CharField(max_length=255)
    # # Um campo que representa a relação genérica que conhece os
    # # campos acima (content_type e object_id)
    # content_object = GenericForeignKey(
    #     'content_type', 'object_id'
    # )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slug(self.name)

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

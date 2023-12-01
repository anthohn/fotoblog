from django.conf import settings
from django.db import models

from PIL import Image

class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    # fk user
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    #redimensionne l'image dans le système de fichiers
    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class Blog(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    # fk user
    date_created = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)
    # Champ pour stocker le nombre de mots dans le contenu du blog
    word_count = models.IntegerField(null=True)
    contributors = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='BlogContributor', related_name='contributions')
    # Fonction interne pour obtenir le nombre de mots dans le contenu du blog
    def _get_word_count(self):
            # Utilise la méthode split pour diviser le contenu en mots, puis renvoie la longueur de la liste résultante
        return len(self.content.split(' '))
    
    # Surcharge de la méthode save pour mettre à jour le nombre de mots avant la sauvegarde
    def save(self, *args, **kwargs):
        # Met à jour word_count avec le nombre de mots obtenus de _get_word_count
        self.word_count = self._get_word_count()
        # Appelle la méthode save de la classe parent pour sauvegarder l'objet
        super().save(*args, **kwargs)

class BlogContributor(models.Model):
    contributor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    contribution = models.CharField(max_length=255, blank=True)
    
    class Meta:
        unique_together = ('contributor', 'blog')
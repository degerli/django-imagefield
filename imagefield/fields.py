from django.db import models
from django.db.models.fields import files

from .widgets import PPOIWidget, with_preview


IMAGE_FIELDS = []


class ImageFieldFile(files.ImageFieldFile):
    def __getattr__(self, key):
        if key in self.field.formats:
            url = '/bla/'  # TODO obviously
            setattr(self, key, url)
            return url
        raise AttributeError('Unknown attribute %r' % key)


class ImageField(models.ImageField):
    attr_class = ImageFieldFile

    def __init__(self, verbose_name=None, **kwargs):
        self.formats = kwargs.pop('formats', None) or {}
        self.ppoi_field = kwargs.pop('ppoi_field', None)

        # TODO implement this? Or handle this outside? Maybe as an image
        # processor? I fear that otherwise we have to reimplement parts of the
        # ImageFileDescriptor (not hard, but too much copy paste for my taste)
        # self.placeholder = kwargs.pop('placeholder', None)

        super().__init__(verbose_name, **kwargs)

        IMAGE_FIELDS.append(self)

    def formfield(self, **kwargs):
        kwargs['widget'] = with_preview(
            kwargs['widget'],
            field_instance=self,
        )
        return super().formfield(**kwargs)


class PPOIField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', '0.5x0.5')
        kwargs.setdefault('max_length', 20)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = PPOIWidget
        return super().formfield(**kwargs)

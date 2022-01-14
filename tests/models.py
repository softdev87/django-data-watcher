from django.db import models

from django_watcher.decorators import watched

from . import watchers


class StubQuerySet(models.QuerySet):
    def __eq__(self, __o: object) -> bool:
        return (
            (
                self.model == __o.model
                and self.query.chain().__str__() == __o.query.chain().__str__()
                and self._db == __o._db
                and self._hints == __o._hints
            )
            if isinstance(__o, models.QuerySet)
            else super().__eq__(__o)
        )


class WatcherModel(models.Model):
    text = models.CharField(max_length=100)

    objects = models.Manager.from_queryset(StubQuerySet)()

    def __eq__(self, __o: object) -> bool:
        if type(self) == type(__o) and self.id is None and __o.id is None:  # noqa
            return self.text == __o.text
        return super().__eq__(__o)

    def __hash__(self):  # noqa
        return super().__hash__()

    class Meta:
        app_label = 'tests'
        abstract = True


@watched(watchers.StubCreateWatcher, ['create'])
class CreateModel(WatcherModel):
    pass


@watched(watchers.StubDeleteWatcher, ['delete'])
class DeleteModel(WatcherModel):
    pass


@watched(watchers.StubSaveWatcher, ['save'])
class SaveModel(WatcherModel):
    pass


@watched(watchers.StubUpdateWatcher, ['update'])
class UpdateModel(WatcherModel):
    pass

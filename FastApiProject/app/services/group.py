from app.repositories.group import GroupRepository
from app.schemas import GroupRead, GroupCreate
from app.exceptions import GroupNotFoundError


class GroupService:
    def __init__(self, group_repo: GroupRepository):
        self.group_repo = group_repo

    async def get_all_groups(self) -> list[GroupRead]:
        groups = await self.group_repo.get_all()
        return [GroupRead.model_validate(g) for g in groups]

    async def get_group_by_slug(self, slug: str):
        group = await self.group_repo.get_by_slug(slug)
        return group

    async def create_group(self, form: GroupCreate) -> GroupRead:
        existing = await self.group_repo.get_by_slug(form.slug)
        if existing:
            raise GroupNotFoundError("Группа с таким slug уже существует")

        group = await self.group_repo.create(
            title=form.title,
            slug=form.slug,
            description=form.description,
        )
        return GroupRead.model_validate(group)
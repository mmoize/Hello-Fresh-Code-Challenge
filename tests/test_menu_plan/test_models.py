from menu_plan.models import Tags


def test_create_tags():
    tag = Tags.objects.create(name="Kids")
    assert tag.name == "Kids"
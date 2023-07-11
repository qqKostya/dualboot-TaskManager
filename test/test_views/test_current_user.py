from test.base import TestViewSetBase


class TestUserViewSet(TestViewSetBase):
    basename = "current_user"

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_retrieve(self):
        user = self.single_resource()
        assert user.get("id") == self.user.id

    def test_patch(self):
        self.patch_single_resource({"first_name": "TestName"})

        user = self.single_resource()
        assert user["first_name"] == "TestName"

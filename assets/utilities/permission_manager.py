from kivy.utils import platform


class PermissionManager:
    @staticmethod
    def request_storage_permissions():
        """ Request storage permissions if platform is android. """

        if platform == "android":
            from android.permissions import request_permissions, Permission

            request_permissions(
                [Permission.WRITE_EXTERNAL_STORAGE, Permission.READ_EXTERNAL_STORAGE]
            )

    def get_default_external_storage(self) -> str:
        """ Request storage permissions and return the primary external storage path (this is the internal one). """

        self.request_storage_permissions()

        if platform == "android":
            from android.storage import primary_external_storage_path

            return primary_external_storage_path()
        else:
            return "~"

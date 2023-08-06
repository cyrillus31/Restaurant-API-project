class NotificationRepository:

    def __init__(self, object_name: str):
        self.object_name = object_name

    def delete_success(self) -> None:
        return {'status': True, 'message': f'The {self.object_name} has been deleted'}

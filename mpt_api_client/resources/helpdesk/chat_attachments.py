from mpt_api_client.http import AsyncService, Service, mixins
from mpt_api_client.models import AttachmentModel


class ChatAttachmentsServiceConfig:
    """Helpdesk Chat Attachments service configuration."""

    _endpoint = "/public/v1/helpdesk/chats/{chat_id}/attachments"
    _model_class = AttachmentModel
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class ChatAttachmentsService(
    mixins.CreateFileMixin[AttachmentModel],
    mixins.UpdateMixin[AttachmentModel],
    mixins.DownloadFileMixin[AttachmentModel],
    mixins.DeleteMixin,
    mixins.GetMixin[AttachmentModel],
    mixins.CollectionMixin[AttachmentModel],
    Service[AttachmentModel],
    ChatAttachmentsServiceConfig,
):
    """Helpdesk Chat Attachments service."""


class AsyncChatAttachmentsService(
    mixins.AsyncCreateFileMixin[AttachmentModel],
    mixins.AsyncUpdateMixin[AttachmentModel],
    mixins.AsyncDownloadFileMixin[AttachmentModel],
    mixins.AsyncDeleteMixin,
    mixins.AsyncGetMixin[AttachmentModel],
    mixins.AsyncCollectionMixin[AttachmentModel],
    AsyncService[AttachmentModel],
    ChatAttachmentsServiceConfig,
):
    """Async Helpdesk Chat Attachments service."""

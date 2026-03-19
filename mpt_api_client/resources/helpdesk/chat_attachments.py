from mpt_api_client.http import AsyncService, Service, mixins
from mpt_api_client.models import Model


class ChatAttachment(Model):
    """Helpdesk Chat Attachment resource."""


class ChatAttachmentsServiceConfig:
    """Helpdesk Chat Attachments service configuration."""

    _endpoint = "/public/v1/helpdesk/chats/{chat_id}/attachments"
    _model_class = ChatAttachment
    _collection_key = "data"
    _upload_file_key = "file"
    _upload_data_key = "attachment"


class ChatAttachmentsService(
    mixins.CreateFileMixin[ChatAttachment],
    mixins.UpdateMixin[ChatAttachment],
    mixins.DownloadFileMixin[ChatAttachment],
    mixins.DeleteMixin,
    mixins.GetMixin[ChatAttachment],
    mixins.CollectionMixin[ChatAttachment],
    Service[ChatAttachment],
    ChatAttachmentsServiceConfig,
):
    """Helpdesk Chat Attachments service."""


class AsyncChatAttachmentsService(
    mixins.AsyncCreateFileMixin[ChatAttachment],
    mixins.AsyncUpdateMixin[ChatAttachment],
    mixins.AsyncDownloadFileMixin[ChatAttachment],
    mixins.AsyncDeleteMixin,
    mixins.AsyncGetMixin[ChatAttachment],
    mixins.AsyncCollectionMixin[ChatAttachment],
    AsyncService[ChatAttachment],
    ChatAttachmentsServiceConfig,
):
    """Async Helpdesk Chat Attachments service."""

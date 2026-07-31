from app.core.config import settings
import logging
import os
import json_log_formatter
from fastapi import Request

class CustomisedJSONFormatter(json_log_formatter.VerboseJSONFormatter):
	def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
		extra['logger'] = 'app'
		# Include builtins
		extra['level'] = record.levelname
		extra['name'] = "{}:{}:{}:{}".format(settings.PROJECT_NAME, settings.DOCKER_HOST,os.getppid(), os.getpid())
		extra['version'] = settings.VERSION
		if 'request_id' in record.__dict__:
			extra['request_id'] = record.__dict__['request_id']

		return super(json_log_formatter.VerboseJSONFormatter, self).json_record(message, extra, record)

class CustomisedUvicornJSONFormatter(json_log_formatter.VerboseJSONFormatter):
	def json_record(self, message: str, extra: dict, record: logging.LogRecord) -> dict:
		extra['logger'] = 'uvicorn'
		# Include builtins
		extra['level'] = record.levelname
		extra['name'] = "{}:{}:{}".format(settings.PROJECT_NAME, settings.DOCKER_HOST, os.getpid())
		extra['version'] = settings.VERSION

		return super(json_log_formatter.VerboseJSONFormatter, self).json_record(message, extra, record)


class SendyLogger(logging.Logger):
	@staticmethod
	def get_extra( request:Request)->dict:
		extra = {}
		tenant_id=request.get('x-tenant-id')
		if tenant_id:
			extra['tenant_id']=tenant_id
		request_id = request.get('x-request-id')
		if request_id:
			extra['request_id']=request_id
		requested_at=request.get('x-requested-at')
		if requested_at:
			extra['requested_at'] = requested_at
		forward_for=request.get('x-forwarded-for')
		if forward_for:
			extra['forward_for']=forward_for
		return extra

	@staticmethod
	def get_logger():
		logger = logging.getLogger(f"{settings.PROJECT_NAME}")
		return logger

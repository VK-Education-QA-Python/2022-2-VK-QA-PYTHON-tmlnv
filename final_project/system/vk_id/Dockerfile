#
FROM python:3.10

#
WORKDIR /vk_id

#
COPY requirements.txt /vk_id/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /vk_id/requirements.txt

#
COPY .. /vk_id

WORKDIR /vk_id

#
CMD ["python3", "fastapi_mock_app.py"]

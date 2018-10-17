from tusclient import client

# Set Authorization headers if it is required
# by the tus server.
my_client = client.TusClient('http://127.0.0.1/storge/tus/')

# Set more headers.
# my_client.set_headers({'HEADER_NAME': 'HEADER_VALUE'})

uploader = my_client.uploader('/Users/taylor/LBPBackend/Backend/upload/1.png', chunk_size=1024 * 1024 * 4, metadata={'filename': '1.png', 'filetype': 'iamge/png'})

# A file stream may also be passed in place of a file path.
# fs = open('/Users/taylor/LBPBackend/Backend/upload/1.png')
# uploader = my_client.uploader(file_stream=fs, chunk_size=200)

# Upload a chunk i.e 200 bytes.
# uploader.upload_chunk()

# Uploads the entire file.
# This uploads chunk by chunk.
uploader.upload()

# # you could increase the chunk size to reduce the
# # number of upload_chunk cycles.
# uploader.chunk_size = 800
# uploader.upload()

# # Continue uploading chunks till total chunks uploaded reaches 1000 bytes.
# uploader.upload(stop_at=1000)

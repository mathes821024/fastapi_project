# FTP服务
import aioftp

async def send_file_to_ftp_server(filename):
    client = aioftp.Client()
    await client.connect("ftp.server.com")
    await client.login("username", "password")
    await client.upload(filename, "/path/on/server/")
    await client.quit()


import os

static_dir = "/home/ubuntu/futboltahmin2/betapp/matches/static/logos"

for file_name in os.listdir(static_dir):
    old_path = os.path.join(static_dir, file_name)
    new_file_name = file_name.lower()
    new_path = os.path.join(static_dir, new_file_name)
    # Eğer isim zaten küçük harf değilse, yeniden adlandır
    if file_name != new_file_name:
        os.rename(old_path, new_path)
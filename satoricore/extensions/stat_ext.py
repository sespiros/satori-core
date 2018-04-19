import os
import stat
from hooker import hook
from satoricore.common import _STANDARD_EXT

ST_MODE_MAPPER = {
    stat.S_IFBLK: _STANDARD_EXT.BLOCK_DEVICE_T,
    stat.S_IFCHR: _STANDARD_EXT.CHAR_DEVICE_T,
    stat.S_IFIFO: _STANDARD_EXT.FIFO_T,
    stat.S_IFLNK: _STANDARD_EXT.LINK_T,
    stat.S_IFSOCK: _STANDARD_EXT.SOCKET_T,
    stat.S_IFLNK: _STANDARD_EXT.LINK_T,
    stat.S_IFREG: _STANDARD_EXT.FILE_T,
}


@hook("pre_open")
def get_stat_info(satori_image, file_path, file_type):
    file_stat = os.lstat(file_path)

    if file_type != _STANDARD_EXT.DIRECTORY_T:
        mode = stat.S_IFMT(file_stat.st_mode)
        file_type = ST_MODE_MAPPER.get(mode, _STANDARD_EXT.UNKNOWN_T)

    stat_dict = {
        'privileges': file_stat.st_mode,
        'uid': file_stat.st_uid,
        'gid': file_stat.st_gid,
        'size': file_stat.st_size,
    }

    times_dict = {
        'atime': file_stat.st_atime,
        'mtime': file_stat.st_mtime,
        'ctime': file_stat.st_ctime,
    }

    satori_image.set_attribute(file_path, file_type, 'type', force_create=True)
    satori_image.set_attribute(file_path, stat_dict, 'stat', force_create=False)
    satori_image.set_attribute(file_path, times_dict, 'times', force_create=False)
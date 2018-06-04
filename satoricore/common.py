from contextlib import contextmanager
import os

from satoricore.logger import logger


class _STANDARD_EXT(object):
    DIRECTORY_T = 'D'
    FILE_T = 'F'
    LINK_T = 'L'
    BLOCK_DEVICE_T = 'B'
    CHAR_DEVICE_T = 'C'
    FIFO_T = 'I'
    SOCKET_T = 'S'
    UNKNOWN_T = 'U'



@contextmanager
def dummy_context(obj):
    yield obj

def get_image_context_from_arg(arg, allow_local=True):

    from satoricore.file import load_image

    if arg == '.':
        return dummy_context(os)

    try:
        os.stat(arg)
        logger.info("Found to '{}'".format(arg))

        image_path = arg
        source = load_image(image_path)
        # print (arg)
        if source != None:
            return dummy_context(source)
    except FileNotFoundError:
        logger.error("File '{}' could not be found".format(arg))
        pass

    try:
        import satoriremote
        logger.info("Connecting to '{}'".format(arg))
        conn_context_source, conn_dict = satoriremote.connect(arg)
        logger.info("[+] Connected to {}".format(
                            conn_dict['host']
                        )
                    )
        return conn_context_source
        # with conn_context_source as context:
        #     return context
    except ImportError:
        logger.error("'satori-remote' package not available, remote paths can't be used")
    except ValueError:  # If can't be parsed as regular expression
        logger.error("'{}' can't be parsed as URI".format(arg))
    except ConnectionError:
        logger.error("Connection failed for path '{}'".format(arg))
        sys.exit(-1)


def load_extension_list(extension_list):
    """
    extension_list: list of filenames 
    """
    for i, extension in enumerate(extension_list):
        try:
            ext_module = imp.load_source(
                'extension_{}'.format(i),
                extension
                )
            logger.info("Extension '{}' loaded".format(ext_module.__name__))
        except Exception as e:
            logger.warning(
                "[-] [{}] - Extension {} could not be loaded".format(
                    e, extension
                )
            )

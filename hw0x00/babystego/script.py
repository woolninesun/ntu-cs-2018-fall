#!/usr/bin/env python2

import binascii

audiotext = '666c61677B74616c6b61746976655f696D6167657D'
print ( bytes.decode( binascii.unhexlify(audiotext) ) )


import UDPmodtager
import Walsh.decoder as decoder

import threading

t2 = threading.Thread(target=UDPmodtager.RSSIplot)

t1.start()
t2.start()
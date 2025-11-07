
def DnC_search(Vinkel1=30, Vinkel2=60, step=4, max_elevation=None, min_elevation=0, angle=0):
            """Simple step-search (divide-and-conquer flavor):
            1) mål RSSI ved Vinkel1 og Vinkel2
            2) vælg den bedst og step i den retning (op hvis Vinkel2 var bedst, ned hvis Vinkel1 var bedst)
            3) stop når RSSI ikke forbedres eller når vi rammer grænser
            Returnerer (best_elevation, best_rssi).
            """         
            TARM.set_pos(angle, Vinkel1)  
            r1 = Beacon_decoder.get_lastest()
            TARM.set_pos(angle, Vinkel2)
            r2 = Beacon_decoder.get_lastest()

            if r2 > r1:
                start = Vinkel2
                direction = 1
                best_rssi = r2
            else:
                start = Vinkel1
                direction = -1
                best_rssi = r1

            best_elev = start
            current_elev = start + direction * step
            while min_elevation <= current_elev <= max_elevation:
                r = Beacon_decoder.get_lastest()
                if r > best_rssi:
                    best_rssi = r
                    best_elev = current_elev
                    current_elev = current_elev + direction * step
                else:
                    break

            return best_elev, best_rssi

def search_initial_location():
    RSSI_array = []
    angle_array = []
    
    def compare_elevations(e1=30, e2=60, angle=0, beams=4, samples=1):
        """Mål RSSI ved to elevationer (e1, e2) på en given azimuth (angle) og returner den bedste.

        Returnerer tuple (best_elevation, rssi_e1, rssi_e2).
        """
        # mål ved e1
        TARM.set_pos(angle, e1)
        r1_vals = []
        for b in range(beams):
            set_switch(b)
            for _ in range(samples):
                r1_vals.append(Beacon_decoder.get_lastest())
        r1 = sum([v for v in r1_vals if v is not None]) / len([v for v in r1_vals if v is not None]) if r1_vals else 0

        # mål ved e2
        TARM.set_pos(angle, e2)
        r2_vals = []
        for b in range(beams):
            set_switch(b)
            for _ in range(samples):
                r2_vals.append(Beacon_decoder.get_lastest())
        r2 = sum([v for v in r2_vals if v is not None]) / len([v for v in r2_vals if v is not None]) if r2_vals else 0

        best = e1 if r1 >= r2 else e2
        return best, r1, r2

    TARM.set_pos(0,30) #Antager at vi kun kan elevation 0-90 grader så vi starter lige på 30 grader og +30 efter
    for angle in range(0, RSSI_angles, 4): #Deler 360 grader op i 4 dele så vi kan gætte os hurtigere frem til den bedste vinkel
        TARM.set_pos(angle,30)
        angle_array.append(angle)
        beam_array = []
        for i in range(4):
            set_switch(i)
            beam_array.append(Beacon_decoder.get_lastest())
        RSSI_array.append(beam_array)
    
    index = np.unravel_index(np.argmax(RSSI_array, axis=None), np.shape(RSSI_array)) # Finder index for max værdi i matrix
    TARM.set_pos(angle_array[index[0]],30) #Sætter antennen til den bedste vinkel fundet vi er kun interesseret i azimuth her
    set_switch(index[1]) #Sætter switchen til den bedste beam fundet
    
    best_elevation, best_rssi = DnC_search(Vinkel1= 30, Vinkel2= 60, step=2, max_elevation=Max_elevation, min_elevation=Min_elevation, angle=angle_array[index[0]])
    TARM.set_pos(angle_array[index[0]], best_elevation)
        
    switch_pos = index[1]
    angle_pos = angle_array[index[0]]
    
    return angle_pos, switch_pos, best_elevation
    
 




"""Acoustics: vibration, sound waves, echoes, pitch, thunder."""

SUBJECT = "physics.acoustics"
SOURCES = ["nasa-glenn-beginners-guide", "noaa-jetstream"]

CONCEPTS = [
    ("vibration", "Mechanical vibration", "A rapid back-and-forth motion of an object such as a string, drumhead or vocal cords.", []),
    ("sound-wave", "Sound wave", "A travelling pattern of compressions and rarefactions in air, water or solids.", []),
    ("medium-needed", "Material medium for sound", "Sound needs particles of air, water or a solid to carry it.", []),
    ("vacuum-silence", "Silence in a vacuum", "In a vacuum no sound can travel because there are no particles to carry it.", []),
    ("sound-speed", "Speed of sound", "Sound travels about 343 metres per second in air at 20 degrees Celsius, faster in water and faster still in solids.", []),
    ("air-temperature-sound", "Warm air carrying sound", "Air at higher temperature.", []),
    ("frequency", "Vibration frequency", "The number of vibrations per second, measured in hertz.", []),
    ("pitch", "Perceived pitch", "How high or low a sound seems; it rises with frequency.", []),
    ("string-tension", "String tension", "How tightly a musical string is stretched.", []),
    ("string-length", "Vibrating string length", "The length of string free to vibrate between fixed points.", []),
    ("amplitude", "Vibration amplitude", "How far the vibrating object or air moves from rest.", []),
    ("loudness", "Perceived loudness", "How loud a sound seems; it grows with amplitude and sound energy.", []),
    ("distance-from-source", "Distance from a sound source", "How far a listener is from the vibrating source.", []),
    ("sound-reflection", "Sound reflection", "Sound bounces off hard surfaces such as walls and cliffs.", []),
    ("echo", "Echo", "A reflected sound heard separately from the original because it arrives noticeably later.", []),
    ("soft-furnishings", "Soft absorbing surfaces", "Curtains, carpets and foam absorb sound energy instead of reflecting it.", []),
    ("doppler-shift", "Doppler pitch shift", "A source moving toward a listener sounds higher in pitch and lower when moving away.", ["doppler effect"]),
    ("moving-source", "Moving sound source", "A sound source travelling relative to the listener.", []),
    ("thunder", "Thunder", "The rumble produced when lightning-heated air expands explosively.", []),
    ("lightning-thunder-delay", "Lightning-to-thunder delay", "Thunder arrives after the flash because sound is far slower than light; about 3 seconds per kilometre.", []),
    ("resonance", "Resonance", "An object driven at its natural frequency vibrates with growing amplitude.", []),
    ("eardrum-vibration", "Eardrum vibration", "Pressure variations of a sound wave set the eardrum vibrating, which the inner ear converts to nerve signals.", []),
    ("hearing-damage", "Noise-induced hearing damage", "Very loud or prolonged sound damages hair cells in the inner ear.", []),
]

RELATIONS = [
    ("vibration-sound", "vibration", "sound-wave", "causes", "Mechanical vibration causes a sound wave in the surrounding medium.", "the vibrating object touches air, water or a solid", ""),
    ("medium-sound", "medium-needed", "sound-wave", "prerequisite", "A material medium for sound is a prerequisite for a sound wave to travel.", "particles are present to compress", ""),
    ("vacuum-sound", "vacuum-silence", "sound-wave", "prevents", "Silence in a vacuum prevents a sound wave from travelling.", "no particles are present", ""),
    ("warm-speed", "air-temperature-sound", "sound-speed", "causes", "Warm air carrying sound causes a higher speed of sound.", "the medium is air", ""),
    ("frequency-pitch", "frequency", "pitch", "causes", "Higher vibration frequency causes higher perceived pitch.", "the frequency is within human hearing", ""),
    ("tension-frequency", "string-tension", "frequency", "causes", "Greater string tension causes higher vibration frequency.", "string length and mass are unchanged", ""),
    ("length-frequency", "string-length", "frequency", "inhibits", "A longer vibrating string length inhibits vibration frequency, giving a lower note.", "tension is unchanged", ""),
    ("amplitude-loudness", "amplitude", "loudness", "causes", "Larger vibration amplitude causes greater perceived loudness.", "the frequency is unchanged", ""),
    ("distance-loudness", "distance-from-source", "loudness", "inhibits", "Greater distance from a sound source inhibits perceived loudness as the energy spreads out.", "the sound spreads freely in open air", ""),
    ("reflection-echo", "sound-reflection", "echo", "causes", "Sound reflection causes an echo when the reflector is far enough away.", "the reflector is more than about 17 metres away", ""),
    ("soft-reflection", "soft-furnishings", "sound-reflection", "inhibits", "Soft absorbing surfaces inhibit sound reflection.", "the surfaces cover a large area", ""),
    ("moving-doppler", "moving-source", "doppler-shift", "causes", "A moving sound source causes a Doppler pitch shift.", "the source moves toward or away from the listener", ""),
    ("thunder-lightning-sound", "thunder", "sound-wave", "causes", "Thunder causes a sound wave that rolls outward from the lightning channel.", "the lightning discharge occurs in air", ""),
    ("speed-delay", "sound-speed", "lightning-thunder-delay", "causes", "The slower speed of sound compared with light causes the lightning-to-thunder delay.", "the observer is away from the strike", ""),
    ("resonance-amplitude", "resonance", "amplitude", "causes", "Resonance causes vibration amplitude to grow.", "the driving frequency matches the natural frequency", "strong damping limits the growth"),
    ("sound-eardrum", "sound-wave", "eardrum-vibration", "causes", "A sound wave causes eardrum vibration.", "the wave reaches the ear", ""),
    ("loudness-damage", "loudness", "hearing-damage", "causes", "Very high perceived loudness causes noise-induced hearing damage.", "the exposure is loud or prolonged enough", ""),
]
